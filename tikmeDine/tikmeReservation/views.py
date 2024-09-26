# tikmeCustomer/views.py
from django.shortcuts import render

def index(request):
    """View function for the home page."""
    return render(request, 'mainCustomer/index.html')


