# tikmeReservation/urls.py
from django.urls import path
from .views import (admin_dashboard, create_reservation)

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('create_reservation/', create_reservation, name='create_reservation'),
]