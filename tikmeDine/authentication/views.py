from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import Employee
from .forms import EmployeeCreationForm, SetupSecurityQuestionsForm, SetupPasswordForm
import logging



logger = logging.getLogger(__name__)

# Publicly accessible portal view
def portal(request):
    logger.debug(f"User accessing portal: {request.path}")
    available_modules = [
        {'name': 'Reservation and Booking System', 'url': '/reservation/admin_login/'},
        {'name': 'Logistics Management System', 'url': '/logistics/admin_login/'},
        {'name': 'Finance Management System', 'url': '/finance/admin_login/'}
    ]
    return render(request, 'portal.html', {'available_modules': available_modules})

# Custom login view for admin access
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/auth/portal/')  # Redirect to portal after successful login
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})  # Handle invalid login
    return render(request, 'admin_login.html')

def system_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('system_admin_dashboard')  # Redirect to system admin dashboard
    return render(request, 'system_admin_login.html')

@login_required
def system_admin_dashboard(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('system_admin_dashboard')
    else:
        form = EmployeeCreationForm()
    
    employees = Employee.objects.all()
    return render(request, 'system_admin_dashboard.html', {'employees': employees, 'form': form})

def change_status(request, employee_id, status):
    employee = Employee.objects.get(id=employee_id)
    employee.account_status = status
    employee.save()
    return redirect('system_admin_dashboard')

def send_email(request, employee_id, email_type):
    employee = Employee.objects.get(id=employee_id)
    email_subject, email_body = "", ""
    
    if email_type == 'onboarding':
        email_subject = "Welcome to [Company/Organization]!"
        email_body = f"""
        Hi {employee.first_name},
        
        Welcome to [Company/Organization]! We’re excited to have you as part of our team.
        
        To complete your account setup, please follow the link below:
        [Complete Account Setup Link]
        
        This link will guide you through the process of setting up your security questions and creating your password. For security purposes, the link is valid for 24 hours. If it expires before you have a chance to set up your account, you can request a new link through our portal.
        
        If you have any questions or need assistance during the setup process, feel free to reach out to us at [Support Email/Phone Number].
        
        We look forward to seeing you on board!
        
        Best regards,
        [Your Name/Team]
        [Company/Organization]
        
        Note: Please do not reply to this email. This mailbox is not monitored.
        """
    elif email_type == 'password_reset':
        email_subject = "Password Reset Request"
        email_body = f"""
        Hi {employee.first_name},
        
        We received a request to reset the password for your account associated with this email address. If you made this request, please click the link below to reset your password:
        [Reset Password Link]
        
        For security reasons, this link will expire in 24 hours. If the link expires, you can request a new one through the "Forgot Password" link on the login page.
        
        If you did not request a password reset, please ignore this email or contact support immediately at [Support Email/Phone].
        
        Thank you,
        [Your Company/Team Name]
        
        Note: Please do not reply to this email. This mailbox is not monitored.
        """
    elif email_type == 'account_unlock':
        email_subject = "Account Unlock Request"
        email_body = f"""
        Hi {employee.first_name},
        
        Your account has been unlocked. Please follow the link below to complete your account setup:
        [Complete Account Setup Link]
        
        This link will guide you through the process of setting up your security questions and creating your password. For security purposes, the link is valid for 24 hours. If it expires before you have a chance to set up your account, you can request a new link through our portal.
        
        If you have any questions or need assistance during the setup process, feel free to reach out to us at [Support Email/Phone Number].
        
        We look forward to seeing you on board!
        
        Best regards,
        [Your Name/Team]
        [Company/Organization]
        
        Note: Please do not reply to this email. This mailbox is not monitored.
        """
    
    send_mail(
        email_subject,
        email_body,
        'from@example.com',
        [employee.email],
        fail_silently=False,
    )
    
    return redirect('system_admin_dashboard')


# Helper function to send the setup email to the new employee
def send_setup_email(employee):
    token = default_token_generator.make_token(employee)
    uid = urlsafe_base64_encode(force_bytes(employee.pk))
    link = reverse('setup_account', kwargs={'uidb64': uid, 'token': token})
    full_link = f"http://127.0.0.1:8000{link}"
    send_mail(
        'Set Up Your Account',
        f'Hello {employee.first_name},\n\nPlease click the link to set up your account: {full_link}\nYour username: {employee.username}\n\nBest regards,\nAdmin Team',
        'tikmedine24@gmail.com',
        [employee.email]
    )

# View to handle account setup based on the unique token
def setup_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = Employee.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        logger.error(f"Employee with UID {uidb64} not found or invalid UID.")
        employee = None

    if employee is not None and default_token_generator.check_token(employee, token):
        if request.method == 'POST':
            form = SetupSecurityQuestionsForm(request.POST)
            if form.is_valid():
                employee.security_answer_1 = form.cleaned_data['security_answer_1']
                employee.security_answer_2 = form.cleaned_data['security_answer_2']
                employee.security_answer_3 = form.cleaned_data['security_answer_3']
                employee.save()
                # Redirect to the password setup view
                return redirect('setup_password', uidb64=uidb64, token=token)
        else:
            form = SetupSecurityQuestionsForm()
        return render(request, 'setup_security_questions.html', {'form': form, 'employee': employee})
    else:
        return render(request, 'invalid_link.html')

def setup_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = Employee.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        employee = None

    if employee is not None and default_token_generator.check_token(employee, token):
        if request.method == 'POST':
            form = SetupPasswordForm(request.POST)
            if form.is_valid():
                employee.set_password(form.cleaned_data['password'])
                employee.save()
                return redirect('admin_login')
            else:
                logger.error(f"Form errors: {form.errors}")
        else:
            form = SetupPasswordForm()
        return render(request, 'setup_password.html', {'form': form, 'employee': employee})
    else:
        return render(request, 'invalid_link.html')
    



