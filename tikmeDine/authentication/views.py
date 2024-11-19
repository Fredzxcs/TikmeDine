# Standard Library Imports
import logging
from datetime import datetime, timedelta
import jwt
import json

# Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

# Django REST Framework Imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

# Local Imports
from .models import Employee
from .forms import EmployeeCreationForm, SetupSecurityQuestionsForm, SetupPasswordForm, TechSupportForm
from .serializers import EmployeeSerializer, SetupSecurityQuestionsSerializer, SetupPasswordSerializer
from authentication.utils import jwt_authenticate 


User = get_user_model()
logger = logging.getLogger(__name__)



# Helper function to generate JWT token for the authenticated user
def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        try:
            login_input = request.POST.get('username', '').strip()  # Username or email
            password = request.POST.get('password', '').strip()
        except (KeyError):
            messages.error(request, 'Invalid data.')
            return redirect('admin_login')

        if not login_input or not password:
            messages.error(request, 'Invalid username or password.')
            return redirect('admin_login')

        # Determine if the login input is an email or username
        user = None
        if '@' in login_input:
            try:
                user = Employee.objects.get(email=login_input)
            except Employee.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return redirect('admin_login')
        else:
            try:
                user = Employee.objects.get(username=login_input)
            except Employee.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                return redirect('admin_login')

        # Authenticate the user
        user = authenticate(request, username=user.username, password=password)
        if user is None:
            messages.error(request, 'Invalid username or password.')
            return redirect('admin_login')

        # Log the user in
        login(request, user)

        # Check the role of the user and redirect accordingly
        if user.is_system_admin():
            return redirect('/api-auth/system_admin_dashboard/')  # Redirect to system admin dashboard
        elif user.is_employee():
            return redirect('/api-admin/admin_dashboard/')  # Redirect to employee dashboard
        else:
            messages.error(request, 'User role is not recognized.')
            return redirect('admin_login')

    return render(request, 'admin_login.html')



# Unauthorized access view
def unauthorized_access(request):
    return render(request, 'unauthorized_access.html')

# invalid or expired token view
def invalid_link(request):
    return render(request, 'invalid_link.html')

def tech_support(request):
    if request.method == 'POST':
        form = TechSupportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data.get('phone_number', 'N/A')
            issue_description = form.cleaned_data['issue_description']
            attachment = request.FILES.get('attachment')

            # Send email
            try:
                send_mail(
                    f'Tech Support Request from {full_name}',
                    f'Issue Details:\n\n{issue_description}\n\nPhone: {phone_number}\nEmail: {email}',
                    email,  # Sender's email
                    ['support@tikmedine.com'],  # Receiver's email (e.g., support team)
                    fail_silently=False,
                )
                # On success, render the success page
                return render(request, 'tech_support.html', {'form': form, 'success': True})
            except Exception as e:
                # If sending the email fails, render the error page
                return render(request, 'tech_support.html', {'form': form, 'error': f'Error sending email: {str(e)}'})

        else:
            # If form validation fails, render with validation errors
            return render(request, 'tech_support.html', {'form': form, 'error': 'Form is not valid.'})

    else:
        form = TechSupportForm()
    return render(request, 'tech_support.html', {'form': form})




def send_reset_password_email(request, employee, is_reset_notification=False):
    # Generate the refresh token (can be used to generate access token too)
    refresh = RefreshToken.for_user(employee)
    access_token = str(refresh.access_token)  # Use the access token for the reset link

    # Encode the employee's primary key for use in the URL
    uid = urlsafe_base64_encode(force_bytes(employee.pk))

    # Build the password reset link with the token
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

    # Send the email
    send_mail(
        email_subject,
        email_body,
        'support@tikmedine.com',
        [employee.email],
        fail_silently=False,
    )
    

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        employee = Employee.objects.filter(email=email).first()

        if employee:
            send_reset_password_email(request, employee)
            messages.success(request, "Password reset link sent to your email.")
        else:
            messages.error(request, "Email is not registered.")

        # Redirect back to the same page to display messages and prevent form resubmission
        return redirect('forgot_password')

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

def admin_dashboard(request):
    # Authenticate the user using the JWT token
    user = jwt_authenticate(request)

    if user:
        try:
            # Get the Employee instance associated with the authenticated user
            employee = Employee.objects.get(username=user.username)

            # Render the dashboard for authenticated employees
            return render(request, 'admin_dashboard.html', {'employee': employee})
        except Employee.DoesNotExist:
            # Handle case where Employee record is not found for the user
            messages.error(request, 'Employee record not found.')
            return render(request, 'unauthorized_access.html')  # Adjusted to render the new template
    else:
        # If JWT token is invalid or expired, return an error message
       messages.error(request, 'Invalid or Expired.Please log in again.')
    return render(request, 'invalid_link.html')  # Render unauthorized access page

def system_admin_dashboard(request):
    # Authenticate the user using the JWT token
    user = jwt_authenticate(request)

    if user:
        # Proceed with the employee list and form handling for system admin
        employees = Employee.objects.all()  # List all employees

        if request.method == 'POST':
            # Check if onboarding email action is requested
            if 'send_onboarding_email' in request.POST:
                employee_id = request.POST.get('employee_id')
                employee = get_object_or_404(Employee, id=employee_id)

                # Send onboarding email
                email_sent = send_onboarding_email(employee.email)
                if email_sent:
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
                return redirect('system_admin_dashboard')

        else:
            form = EmployeeCreationForm()

        # Render the system admin dashboard with employee data and form
        return render(request, 'system_admin_dashboard.html', {'employees': employees, 'form': form})

    # If user is not authenticated, redirect to login
    return redirect('admin_login')

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