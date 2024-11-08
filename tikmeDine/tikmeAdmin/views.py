from django.shortcuts import render


# Authentication
def admin_login(request):
    return render(request, 'admin_login.html')
# dashboard view
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
# create reservation
def create_reservation(request):
    return render(request, 'create_reservation.html')
