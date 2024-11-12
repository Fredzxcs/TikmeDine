# urls.py

from django.urls import path  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    # Admin Actions
    admin_login,
    send_reset_password_email,

    # Password Management
    forgot_password,
    reset_password,

    # Additional Views
    system_admin_dashboard,
    add_employee,
    change_status,
    
    # Email Actions
    send_onboarding_email,
    send_account_reactivation_email,
    
    # Account Setup
    setup_account,
    setup_password,
    setup_security_questions,
    
    # Password Management
    reactivate_account,

    # Additional Views
    send_account_locked_email,
    send_permanently_locked_email,
    jwt_authenticate,
    
)

urlpatterns = [

    path('admin_login/', admin_login, name='admin_login'),
    path('send_reset_password_email/<int:employee_id>/', send_reset_password_email, name='send_reset_password_email'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),

    # Admin Routes
    path('system_admin_dashboard/', system_admin_dashboard, name='system_admin_dashboard'),
    path('add_employee/', add_employee, name='add_employee'),
    path('change_status/<int:employee_id>/<str:status>/', change_status, name='change_status'),

    # Email Actions
    path('send_onboarding_email/<int:employee_id>/', send_onboarding_email, name='send_onboarding_email'),
    path('send_account_reactivation_email/<int:employee_id>/', send_account_reactivation_email, name='send_account_reactivation_email'),

    # Account Setup
    path('setup_account/<uidb64>/<token>/', setup_account, name='setup_account'),
    path('setup_password/<uidb64>/<token>/', setup_password, name='setup_password'),
    path('setup_security_questions/', setup_security_questions, name='setup_security_questions'),

    # Password Management
    path('reactivate_account/<uidb64>/<token>/', reactivate_account, name='reactivate_account'),


    path('send_account_locked/<int:employee_id>/', send_account_locked_email, name='send_account_locked_email'),
    path('send_permanently_locked/<int:employee_id>/', send_permanently_locked_email, name='send_permanently_locked_email'),
    path('jwt_authenticate/', jwt_authenticate, name='jwt_authenticate'),

    # JWT Token Routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # Endpoint for obtaining access and refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # Endpoint for refreshing access tokens
 
]
