# tikmeReservation/views.py
from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def create_reservation(request):
    return render(request, 'create_reservation.html')