# authentication/urls.py
from django.urls import path
from .views import create_employee, setup_account, setup_password, admin_login, portal

urlpatterns = [
    path('create_employee/', create_employee, name='create_employee'),
    path('setup/<uidb64>/<token>/', setup_account, name='setup_account'),
    path('setup_password/<uidb64>/<token>/', setup_password, name='setup_password'),
    path('admin_login/', admin_login, name='admin_login'),
    path('', portal, name='portal'),
]

