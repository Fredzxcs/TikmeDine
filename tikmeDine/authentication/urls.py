# authentication/urls.py
from django.urls import path
from .views import setup_account, setup_password, admin_login, portal, system_admin_login, system_admin_dashboard,change_status, send_email

urlpatterns = [
    path('', portal, name='portal'),
    path('admin_login/', admin_login, name='admin_login'),
    path('system_admin_login/', system_admin_login, name='system_admin_login'),
    path('system_admin_dashboard/', system_admin_dashboard, name='system_admin_dashboard'),
    path('change_status/<int:employee_id>/<str:status>/', change_status, name='change_status'),
    path('send_email/<int:employee_id>/<str:email_type>/', send_email, name='send_email'),
    path('setup/<uidb64>/<token>/', setup_account, name='setup_account'),
    path('setup_password/<uidb64>/<token>/', setup_password, name='setup_password'),
]


