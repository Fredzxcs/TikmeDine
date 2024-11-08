from django.urls import path
from .views import (
    admin_login,
    admin_dashboard,
    create_reservation

)


urlpatterns = [
    # Authentication
    path('', admin_login, name='admin_login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create_reservation/', create_reservation, name='create_reservation'),
]