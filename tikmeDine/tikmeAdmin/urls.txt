# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
 
    # Admin Views
    admin_login,

    # Email Actions
    send_reset_password_email,

    # Password Management
    forgot_password,
    reset_password,

    # Additional Views
    jwt_authenticate,
    

)

urlpatterns = [
  path('admin_login/', admin_login, name='admin_login'),
  path('send_reset_password_email/<int:employee_id>/', send_reset_password_email, name='send_reset_password_email'),
  path('forgot_password/', forgot_password, name='forgot_password'),
  path('reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),
  path('jwt_authenticate/', jwt_authenticate, name='jwt_authenticate'),

  # JWT Token Routes
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      
]