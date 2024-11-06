<<<<<<< HEAD
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


# Function to generate access and refresh tokens using Simple JWT
def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

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

    return access_token, refresh_token
# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            access_token, refresh_token = generate_tokens(user)
            request.session['jwtToken'] = access_token
            return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token, 'redirect_url': '/admin_dashboard/'})
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

=======
# tikmeReservation/views.py
from django.shortcuts import render
>>>>>>> 32624d54abe0064c6fc4ff8e7d5dc0df463c0d3f

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
<<<<<<< HEAD
=======

def create_reservation(request):
    return render(request, 'create_reservation.html')
>>>>>>> 32624d54abe0064c6fc4ff8e7d5dc0df463c0d3f
