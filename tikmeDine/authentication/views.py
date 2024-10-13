from django.shortcuts import render
def adminAuthentication(request):
    """View function for the authentication page."""
    return render(request, 'adminAuthentication.html')
