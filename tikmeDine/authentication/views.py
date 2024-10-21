from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import Employee
from .forms import EmployeeCreationForm, SetupAccountForm

@login_required
def portal(request):
    user = request.user
    available_modules = [
        {'name': 'Reservation and Booking System', 'url': '/reservation/admin_login/'},
        {'name': 'Logistics Management System', 'url': '/logistics/admin_login/'},
        {'name': 'Finance Management System', 'url': '/finance/admin_login/'}
    ]
    return render(request, 'portal.html', {'available_modules': available_modules})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/tikmeAdmin/admin_dashboard/')
    return render(request, 'admin_login.html')

def create_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.set_unusable_password()
            employee.save()
            send_setup_email(employee)
            return redirect('admin_dashboard')
    else:
        form = EmployeeCreationForm()
    return render(request, 'create_employee.html', {'form': form})

def send_setup_email(employee):
    token = default_token_generator.make_token(employee)
    uid = urlsafe_base64_encode(force_bytes(employee.pk))
    link = reverse('setup_account', kwargs={'uidb64': uid, 'token': token})
    full_link = f"https://tikmedine.com{link}"
    send_mail(
        'Set Up Your Account',
        f'Hello {employee.first_name},\n\nPlease click the link to set up your account: {full_link}\nYour username: {employee.username}\n\nBest regards,\nAdmin Team',
        'tikmedine24@gmail.com',
        [employee.email]
    )

def setup_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        employee = Employee.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
        employee = None

    if employee is not None and default_token_generator.check_token(employee, token):
        if request.method == 'POST':
            form = SetupAccountForm(request.POST)
            if form.is_valid():
                employee.set_password(form.cleaned_data['password'])
                employee.security_question_1 = form.cleaned_data['security_question_1']
                employee.security_answer_1 = form.cleaned_data['security_answer_1']
                employee.security_question_2 = form.cleaned_data['security_question_2']
                employee.security_answer_2 = form.cleaned_data['security_answer_2']
                employee.security_question_3 = form.cleaned_data['security_question_3']
                employee.security_answer_3 = form.cleaned_data['security_answer_3']
                employee.save()
                return redirect('admin_login')
        else:
            form = SetupAccountForm()
        return render(request, 'setup_account.html', {'form': form, 'employee': employee})
    else:
        return render(request, 'invalid_link.html')
