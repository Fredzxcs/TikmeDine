# tikmeCustomer/views.py
from django.shortcuts import render

def home(request):
    """View function for the home page."""
    return render(request, 'mainCustomer/home.html')


