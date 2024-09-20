# tikmeCustomer/views.py
from django.shortcuts import render

def home(request):
    """View function for the home page."""
    return render(request, 'mainCustomer/home.html')

def menu(request):
    """View function for the menu page."""
    return render(request, 'mainCustomer/menu.html')

def reservation(request):
    """View function for the reservation page."""
    return render(request, 'mainCustomer/reservation.html')

def faq(request):
    """View function for the faq page."""
    return render(request, 'mainCustomer/faq.html')

def contact(request):
    """View function for the contact page."""
    return render(request, 'mainCustomer/contact.html')

