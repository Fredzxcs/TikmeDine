# authentication/urls.py
from django.urls import path
from .views import create_employee, setup_account, admin_login, portal

urlpatterns = [
    path('create_employee/', create_employee, name='create_employee'),
    path('setup/<uidb64>/<token>/', setup_account, name='setup_account'),
    path('admin_login/', admin_login, name='admin_login'),  # Custom login view
    path('portal/', portal, name='portal'),  # Publicly accessible portal
]

