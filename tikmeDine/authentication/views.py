# Standard Library Imports
import logging
from datetime import datetime, timedelta
import jwt

# Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required   
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from django.contrib import messages


# Django REST Framework Imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework import status

# Local Imports
from .models import Employee
from .forms import EmployeeCreationForm, SetupSecurityQuestionsForm, SetupPasswordForm
from .serializers import EmployeeSerializer, SetupSecurityQuestionsSerializer, SetupPasswordSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


# Function to generate access and refresh tokens using Simple JWT
def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

# Standard Library Imports
import logging
from datetime import datetime, timedelta
import jwt

# Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required   
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


# Django REST Framework Imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework import status

# Local Imports
from authentication .models import Employee
from authentication .forms import EmployeeCreationForm, SetupSecurityQuestionsForm, SetupPasswordForm
from authentication .serializers import EmployeeSerializer, SetupSecurityQuestionsSerializer, SetupPasswordSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


# Admin login view
# Admin login view (handling both system admin and regular admin login)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate tokens for the user
            access_token, refresh_token = generate_tokens(user)
            request.session['jwtToken'] = access_token
            
            # Fetch the employee data from the Employee model (assuming this model has a role field)
            try:
                employee = Employee.objects.get(user=user)
            except Employee.DoesNotExist:
                return JsonResponse({'error': 'Employee not found'}, status=404)
            
            # Check the user's role and determine the redirect URL
            if employee.role == 'system_admin':  # Example role check for system admin
                redirect_url = '/api-auth/system_admin_dashboard/'
            else:
                redirect_url = '/admin_dashboard/'

            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect_url': redirect_url
            })
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

    return render(request, 'admin_login.html')



def send_reset_password_email(request, employee, is_reset_notification=False):
    access_token, _ = generate_tokens(employee)  # Generate only the access token for the link
    uid = urlsafe_base64_encode(force_bytes(employee.pk))
    link = reverse('reset_password', kwargs={'uidb64': uid, 'token': access_token})
    full_link = f"https://{request.get_host()}{link}"

    # Email content setup
    email_subject = "Password Reset Request" if not is_reset_notification else "Password Successfully Reset"
    email_body = f"""
    Dear {employee.first_name},

    Please use the following link to reset your password:
    {full_link}

    Best Regards,
    Tikme Dine Team
    """

    send_mail(
        email_subject,
        email_body,
        'support@tikmedine.com',
        [employee.email],
        fail_silently=False,
    )
    
@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        employee = Employee.objects.filter(email=email).first()
        
        if employee:
            send_reset_password_email(request, employee)
            return JsonResponse({"message": "Password reset link sent to your email."})
        else:
            return JsonResponse({"error": "Email is not registered."}, status=404)
    return render(request, 'forgot_password.html')


@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = get_object_or_404(Employee, pk=uid)
        RefreshToken(token)  # JWT verification
    except Exception:
        employee = None

    if employee and request.method == 'POST':
        password_form = SetupPasswordForm(request.POST)
        if password_form.is_valid():
            employee.set_password(password_form.cleaned_data['password'])
            employee.save()
            return redirect('login')
    else:
        password_form = SetupPasswordForm()

    return render(request, 'reset_password.html', {'password_form': password_form})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Ensure this checks the token
def system_admin_dashboard(request):
    # Authenticate the user using the JWT token
    user = jwt_authenticate(request)
    
    if user:
        employees = Employee.objects.all()

        if request.method == 'POST':
            # Check if onboarding email action is requested
            if 'send_onboarding_email' in request.POST:
                employee_id = request.POST.get('employee_id')
                employee = get_object_or_404(Employee, id=employee_id)
                
                # Send onboarding email (assuming the function returns a success boolean)
                if send_onboarding_email(employee.email):
                    messages.success(request, 'Onboarding email sent successfully.')
                else:
                    messages.error(request, 'Failed to send onboarding email.')
                    
                return redirect('system_admin_dashboard')  # Redirect to avoid form resubmission
            
            # Handle employee creation or update
            employee_id = request.POST.get('employee_id')
            employee = get_object_or_404(Employee, id=employee_id) if employee_id else None
            
            form = EmployeeCreationForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('system_admin_dashboard')  # Redirect to refresh the employee list
        else:
            form = EmployeeCreationForm()

        # Render the dashboard with employee data, the form, and success messages
        return render(request, 'system_admin_dashboard.html', {'employees': employees, 'form': form})

    # Render login page if not authenticated
    return render(request, 'system_admin_login.html', {'error': 'Authentication required.'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_employee(request, employee_id=None):
    user = jwt_authenticate(request)
    if user:
        employee = get_object_or_404(Employee, id=employee_id) if employee_id else None
        if request.method == 'POST':
            form = EmployeeCreationForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('system_admin_dashboard')
        else:
            form = EmployeeCreationForm(instance=employee)
        return render(request, 'system_admin_dashboard.html', {'form': form, 'employee': employee})
    return Response({"detail": "Authentication credentials were not provided."}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_status(request, employee_id, status):
    user = jwt_authenticate(request)
    if user:
        employee = get_object_or_404(Employee, id=employee_id)

        valid_transitions = {
            'active': ['inactive', 'suspended'],
            'inactive': ['active'],
            'suspended': ['active']
        }

        if status in valid_transitions.get(employee.account_status, []):
            employee.account_status = status
            employee.save()
        else:
            return redirect('system_admin_dashboard')

        return redirect('system_admin_dashboard')
    return Response({"detail": "Authentication credentials were not provided."}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_onboarding_email(request, employee_id):
    user = jwt_authenticate(request)  # Ensure this function exists to validate the JWT token
    if user:
        employee = get_object_or_404(Employee, id=employee_id)

        # Create a JWT token for the employee
        token = AccessToken.for_user(employee)  # Generate a JWT token
        uid = urlsafe_base64_encode(force_bytes(employee.pk))  # Encode the user ID
        link = reverse('setup_account', kwargs={'uidb64': uid, 'token': str(token)})  # Create the setup account link
        full_link = request.build_absolute_uri(link)  # Dynamically get the full URL

        email_subject = "Welcome to Tikme Dine!"    

        email_body = f"""
        Hi {employee.first_name},

        Welcome to Tikme Dine! We’re thrilled to have you as part of our team.

        To complete your account setup, please follow the link below:
        {full_link}

        This link will guide you through the process of setting up your security questions and creating your password. For security purposes, the link is valid for 24 hours.

        If you have any questions or need assistance, feel free to reach out.

        Best regards,  
        Fred  
        Tikme Dine Team
        """

        # Send the email
        try:
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,  # Use a sender email from settings
                [employee.email],
            )
            return Response({"detail": "Email sent successfully."}, status=200)
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")  # Log the error
            return Response({"detail": "Error sending email."}, status=500)
        
    return Response({"detail": "Authentication credentials were not provided."}, status=401)


# Reactivation of account using JWT for authentication
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def reactivate_account(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = Employee.objects.get(pk=uid)  # Get the employee by ID
    except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        employee = None

    # Validate the JWT token
    try:
        # Decode the token and validate it
        AccessToken(token)  # This will raise an error if the token is invalid
    except TokenError:
        return render(request, 'invalid_link.html')  # Token is invalid, show error page

    if employee is not None:  # If employee is found
        if request.method == 'POST':
            form = SetupPasswordForm(request.POST)
            if form.is_valid():
                employee.set_password(form.cleaned_data['password'])  # Set new password
                employee.save()  # Save the employee instance
                return redirect('admin_login')  # Redirect to login page
            else:
                logger.error(f"Form errors: {form.errors}")
        else:
            form = SetupPasswordForm()
        
        return render(request, 'reactivate_account.html', {'form': form, 'employee': employee})  # Render reactivation form
    else:
        return render(request, 'invalid_link.html')  # Employee not found, show error page
    []
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_account_reactivation_email(request, employee_id, lock_type=None):
    user = jwt_authenticate(request)
    if user:
        employee = get_object_or_404(Employee, id=employee_id)
        
        if lock_type == 'temporary':
            send_account_locked_email(employee)
        elif lock_type == 'permanent':
            send_permanently_locked_email(employee)
        else:
            # Logic to send account reactivation email
            send_reactivation_confirmation_email(employee)
            
        return redirect('system_admin_dashboard')
    
    return Response({"detail": "Authentication credentials were not provided."}, status=401)

def send_account_locked_email(employee):
    email_subject = "Account Temporarily Locked"
    email_body = f"""
    Hi {employee.first_name},

    Your account has been temporarily locked due to multiple incorrect attempts. It will be locked for 15 minutes. If you did not request this, please contact support.

    Thank you,
    [Your Company/Team Name]
    """
    send_mail(email_subject, email_body, 'support@tikmedine.com', [employee.email], fail_silently=False)

def send_permanently_locked_email(employee):
    email_subject = "Account Permanently Locked"
    email_body = f"""
    Hi {employee.first_name},

    Your account has been permanently locked due to multiple incorrect attempts within 24 hours. Please contact support to unlock your account.

    Thank you,
    [Your Company/Team Name]
    """
    send_mail(email_subject, email_body, 'support@tikmedine.com', [employee.email], fail_silently=False)

# Email notification for account reactivation
def send_reactivation_confirmation_email(employee):
    email_subject = "Password Successfully Set for Your Tikme Dine Account"
    email_body = f"""
    Dear {employee.first_name},

    We wanted to let you know that the password for your Tikme Dine account has been successfully set.
    Date and Time of Change: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    If you did not request this change, please contact our support team immediately at support@tikmedine.com.

    You can log in to your account here: [Insert Login Page Link]

    Best Regards,
    The Tikme Dine Team
    """
    send_mail(
        email_subject,
        email_body,
        'support@tikmedine.com',
        [employee.email],
        fail_silently=False,
    )



# Helper function to authenticate via JWT   
def jwt_authenticate(request):
    auth = get_authorization_header(request).split()
    if len(auth) == 2 and auth[0].lower() == b'bearer':
        token = auth[1].decode('utf-8')  # Decode bytes to string
        try:
            # Validate and decode the token
            valid_token = JWTAuthentication().get_validated_token(token)
            return JWTAuthentication().get_user(valid_token)
        except Exception as e:
            logger.error(f"JWT Authentication error: {e}")
            return None
    logger.warning("No authorization header or incorrect format.")
    return None


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def setup_account(request, uidb64, token):
    # Store the token in session
    request.session['jwt_token'] = token

    # Decode the UID and verify the user as before
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = Employee.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        employee = None

    try:
        decoded_token = jwt.decode(request.session['jwt_token'], settings.SECRET_KEY, algorithms=["HS256"])
        if str(employee.pk) != str(decoded_token['user_id']):
            return render(request, 'invalid_link.html')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return render(request, 'invalid_link.html')

    form = SetupSecurityQuestionsForm()
    return render(request, 'setup_security_questions.html', {
        'form': form,
        'employee': employee
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def setup_security_questions(request):
    user = jwt_authenticate(request)
    if not user:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':
        serializer = SetupSecurityQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=user)
                return Response({
                    "success": True,
                    "redirect_url": "/setup-password"  # Adjust to your URL name
                })
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    form = SetupSecurityQuestionsForm()
    return render(request, 'setup_security_questions.html', {"form": form, "user": user})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def setup_password(request):
    # Check if the user is authenticated
    user = jwt_authenticate(request)
    if not user:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':
        form = SetupPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return Response({"success": "Password setup successful!"}, status=status.HTTP_200_OK)

    return render(request, 'setup_password.html', {'form': SetupPasswordForm()})