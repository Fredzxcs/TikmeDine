from django.shortcuts import render
def adminAuthentication(request):
    """View function for the authentication page."""
    return render(request, 'adminAuthentication.html')

def adminPortal(request):
    """View function for the authentication page."""
    return render(request, 'adminPortal.html')
