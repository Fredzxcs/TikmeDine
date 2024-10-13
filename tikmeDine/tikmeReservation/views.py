from django.shortcuts import render

def tikmeCustomer(request):
    """View function for the home page."""
    return render(request, 'tikmeCustomer.html')



