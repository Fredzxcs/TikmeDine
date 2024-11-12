from django.shortcuts import render



# dashboard view
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
# create reservation
def create_reservation(request):
    return render(request, 'create_reservation.html')
