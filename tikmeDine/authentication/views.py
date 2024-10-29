# Standard Library Imports
import logging
import datetime

# Django Core Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse

from django.http import JsonResponse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Date and Time Utilities
from datetime import timedelta

# Django REST Framework Imports
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header

# Local Imports
from .models import Employee
from .forms import EmployeeCreationForm, SetupSecurityQuestionsForm, SetupPasswordForm


User = get_user_model()
logger = logging.getLogger(__name__)

def portal(request):
    logger.debug(f"User accessing portal: {request.path}")
    available_modules = [
        {'name': 'Reservation and Booking System', 'url': '/reservation/admin_login/'},
        {'name': 'Logistics Management System', 'url': '/logistics/admin_login/'},
        {'name': 'Finance Management System', 'url': '/finance/admin_login/'},
        {'name': 'System Admin', 'url': '/auth/system_admin_login/'}
    ]
    return render(request, 'portal.html', {'available_modules': available_modules})

# Custom login view for admin access
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT token instead of using Django session authentication
            token = generate_jwt_token(user)
            return JsonResponse({'token': token})  # Return the token on successful login
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})  # Handle invalid login
    return render(request, 'admin_login.html')

def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def forgot_password(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        employee = Employee.objects.filter(email=email).first()
        
        if employee:
            send_reset_password_email_logic(request, employee)
            return JsonResponse("Password reset link sent to your email.")
        else:
            error_message = "This email is not registered yet in the system."

    return render(request, 'forgot_password.html', {'error_message': error_message})

@login_required
def setup_password(request, uidb64, token):
    try:
        # Decode UID
        uid = force_str(urlsafe_base64_decode(uidb64))
        employee = User.objects.get(pk=uid)
        
        # Validate JWT token
        access_token = AccessToken(token)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, TokenError):
        employee = None

    if employee is not None and access_token:
        if request.method == 'POST':
            form = SetupPasswordForm(request.POST)
            if form.is_valid():
                employee.set_password(form.cleaned_data['password'])
                employee.save()
                return redirect('login')  # Redirect to login after successful password setup
        else:
            form = SetupPasswordForm()
    else:
        form = None

    return render(request, 'setup_password.html', {
        'form': form,
        'uidb64': uidb64,
        'token': token,
        'employee': employee,
    })


def send_reset_password_email_logic(request, employee):
    token = generate_jwt_token(employee)
    uid = urlsafe_base64_encode(force_bytes(employee.pk))
    link = reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
    full_link = f"https://{request.get_host()}{link}"

    email_subject = "Password Reset Request"
    email_body = f"""
    Hi {employee.first_name},

    We received a request to reset the password for your account associated with this email address. If you made this request, please click the link below to reset your password:
    {full_link}

    For security reasons, this link will expire in 15 minutes. If the link expires, you can request a new one through the "Forgot Password" link on the login page.

    If you did not request a password reset, please ignore this email or contact support immediately at [Support Email/Phone].

    Thank you,
    [Your Company/Team Name]

    Note: Please do not reply to this email. This mailbox is not monitored.
    """
    send_mail(
        email_subject,
        email_body,
        'tikmedine24@gmail.com',  # Replace with your sender email
        [employee.email],
    )

@api_view(['GET', 'POST'])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        employee = get_object_or_404(User, pk=uid)
        # Validate JWT token
        RefreshToken(token)
    except Exception as e:
        employee = None

    if employee:
        if request.method == 'POST':
            if 'verify_security' in request.POST:
                form = SetupSecurityQuestionsForm(request.POST)
                if form.is_valid():
                    if (employee.security_answer_1 == form.cleaned_data['security_answer_1'] and 
                        employee.security_answer_2 == form.cleaned_data['security_answer_2'] and 
                        employee.security_answer_3 == form.cleaned_data['security_answer_3']):
                        
                        # Security questions are correct, show password form
                        password_form = SetupPasswordForm()
                        return render(request, 'reset_password.html', {
                            'form': form,
                            'password_form': password_form,
                            'uidb64': uidb64,
                            'token': token,
                        })
                    else:
                        employee.failed_attempts += 1
                        employee.last_failed_attempt = timezone.now()

                        if employee.failed_attempts >= 3:
                            # Lock the account temporarily for 15 minutes
                            if employee.last_failed_attempt + timedelta(minutes=15) < timezone.now():
                                employee.failed_attempts = 0  # Reset attempts after 15 minutes
                            else:
                                employee.account_status = 'locked'
                                send_account_locked_email(employee)
                                return render(request, 'account_locked.html', {})

                        if employee.failed_attempts >= 9:  # 3 sets of 3 attempts in 24 hours
                            employee.account_status = 'inactive'
                            employee.failed_attempts = 0  # Reset attempts
                            send_permanently_locked_email(employee)

                        employee.save()
                        form.add_error(None, 'Incorrect answers. Try again.')
            else:
                form = SetupSecurityQuestionsForm()
                password_form = SetupPasswordForm(request.POST)
                if password_form.is_valid():
                    employee.set_password(password_form.cleaned_data['password'])
                    employee.save()
                    return redirect('login')
        else:
            form = SetupSecurityQuestionsForm()
            password_form = None
    else:
        form = None
        password_form = None

    return render(request, 'reset_password.html', {
        'form': form,
        'password_form': password_form,
        'uidb64': uidb64,
        'token': token,
    })

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

def send_reset_password_email_confirmation(request, employee):
    import datetime
    token = generate_jwt_token(employee)
    uid = urlsafe_base64_encode(force_bytes(employee.pk))
    link = reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
    full_link = f"http://{request.get_host()}{link}"

    email_subject_setup = "Security Questions Setup Complete"
    email_body_setup = f"""
    Hi {employee.first_name},

    Your security questions have been set up successfully. You can now reset your password using the link below if needed:
    {full_link}

    For security reasons, this link will expire in 24 hours. If the link expires, you can request a new one through the "Forgot Password" link on the login page.

    If you did not request this, please contact support immediately at [Support Email/Phone].

    Thank you,
    [Your Company/Team Name]

    Note: Please do not reply to this email. This mailbox is not monitored.
    """
    send_mail(
        email_subject_setup,
        email_body_setup,
        'tikmedine24@gmail.com',  # Replace with your sender email
        [employee.email],
    )

    email_subject_reset = "Password Successfully Reset for Your Tikme Dine Account"
    email_body_reset = f"""
    Dear {employee.first_name},

    We wanted to let you know that the password for your Tikme Dine account has been successfully reset.

    Date and Time of Change: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    If you did not request this change, please contact our support team immediately at support@tikmedine.com.

    You can log in to your account here: [Insert Login Page Link]

    Best Regards,
    The Tikme Dine Team
    """
    send_mail(
        email_subject_reset,
        email_body_reset,
        'support@tikmedine.com',  # Replace with your sender email
        [employee.email],
        fail_silently=False,
    )

def system_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT token for system admin
            token = generate_jwt_token(user)
            return JsonResponse({'token': token, 'redirect_url': '/system_admin_dashboard/'})  # Include the token and redirect URL
        else:
            return render(request, 'system_admin_login.html', {'error': 'Invalid username or password'})  # Handle invalid login
    return render(request, 'system_admin_login.html')


# Helper function to authenticate via JWT
def jwt_authenticate(request):
    auth = get_authorization_header(request).split()
    if len(auth) == 2 and auth[0].lower() == b'bearer':
        token = auth[1]
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
@permission_classes([IsAuthenticated])  # Make sure this checks the token
def system_admin_dashboard(request):
    # Authenticate the user using the JWT token
    user = jwt_authenticate(request)
    
    if user:
        employees = Employee.objects.all()

        if request.method == 'POST':
            employee_id = request.POST.get('employee_id')
            employee = get_object_or_404(Employee, id=employee_id) if employee_id else None
            
            form = EmployeeCreationForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('system_admin_dashboard')  # Redirect to refresh the employee list
        else:
            form = EmployeeCreationForm()

        # Render the dashboard with employee data and the form
        return render(request, 'system_admin_dashboard.html', {'employees': employees, 'form': form})

    return render(request, 'system_admin_login.html', {'error': 'Authentication required.'})  # Redirect to login if not authenticated

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_onboarding_email(request, employee_id):
    user = jwt_authenticate(request)
    if user:
        employee = get_object_or_404(Employee, id=employee_id)
        onboarding_email(employee)
        return redirect('system_admin_dashboard')
    return Response({"detail": "Authentication credentials were not provided."}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_account_reactivation_email(request, employee_id):
    user = jwt_authenticate(request)
    if user:
        employee = get_object_or_404(Employee, id=employee_id)
        # Logic to send account reactivation email
        return redirect('system_admin_dashboard')
    return Response({"detail": "Authentication credentials were not provided."}, status=401)

def onboarding_email(employee):
    # Create a JWT token for the employee
    token = AccessToken.for_user(employee)  # Generate a JWT token
    uid = urlsafe_base64_encode(force_bytes(employee.pk))  # Encode the user ID
    link = reverse('setup_account', kwargs={'uidb64': uid, 'token': str(token)})  # Create the setup account link
    full_link = f"http://127.0.0.1:8000{link}"

    email_subject = "Welcome to [Company/Organization]!"
    email_body = f"""
    Hi {employee.first_name},

    Welcome to [Company/Organization]! We’re excited to have you as part of our team.

    To complete your account setup, please follow the link below:
    {full_link}

    This link will guide you through the process of setting up your security questions and creating your password. For security purposes, the link is valid for 24 hours.

    If you have any questions or need assistance, feel free to reach out.

    Best regards,
    [Your Name/Team]
    [Company/Organization]
    """
    
    send_mail(
        email_subject,
        email_body,
        'tikmedine24@gmail.com',
        [employee.email],
    )


def setup_account(request, uidb64, token):
    try:
        # Decode the UID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        # Retrieve the employee object
        employee = Employee.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        employee = None

    # Verify the JWT token
    try:
        decoded_token = AccessToken(token)
        # Here, you might also want to check if the token belongs to the employee
        if str(employee.pk) != decoded_token['user_id']:
            return render(request, 'invalid_link.html')
    except TokenError:
        return render(request, 'invalid_link.html')

    if employee is not None:
        if request.method == 'POST':
            form = SetupSecurityQuestionsForm(request.POST)
            if form.is_valid():
                employee.security_answer_1 = form.cleaned_data['security_answer_1']
                employee.security_answer_2 = form.cleaned_data['security_answer_2']
                employee.security_answer_3 = form.cleaned_data['security_answer_3']
                employee.save()
                return redirect('setup_password', uidb64=uidb64, token=token)
        else:
            form = SetupSecurityQuestionsForm()
        return render(request, 'setup_security_questions.html', {'form': form, 'employee': employee})
    else:
        return render(request, 'invalid_link.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def setup_security_questions(request):
    user = jwt_authenticate(request)
    if user:
        if request.method == 'POST':
            form = SetupSecurityQuestionsForm(request.POST)
            if form.is_valid():
                employee = request.user
                employee.security_question_1 = form.cleaned_data['security_question_1']
                employee.security_answer_1 = form.cleaned_data['security_answer_1']
                employee.security_question_2 = form.cleaned_data['security_question_2']
                employee.security_answer_2 = form.cleaned_data['security_answer_2']
                employee.security_question_3 = form.cleaned_data['security_question_3']
                employee.security_answer_3 = form.cleaned_data['security_answer_3']
                employee.account_status = 'active'
                employee.save()

                send_reset_password_confirmation_email(employee)
                return redirect('system_admin_dashboard')
        else:
            form = SetupSecurityQuestionsForm()
        return render(request, 'setup_security_questions.html', {'form': form})
    return Response({"detail": "Authentication credentials were not provided."}, status=401)

# Email notification for password reset
def send_reset_password_confirmation_email(employee):
    email_subject = "Password Successfully Reset for Your Tikme Dine Account"
    email_body = f"""
    Dear {employee.first_name},

    We wanted to let you know that the password for your Tikme Dine account has been successfully reset.
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