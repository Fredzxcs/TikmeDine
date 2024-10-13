from django.shortcuts import render
def adminDashboard(request):
    """View function for the home page."""
    return render(request, 'adminDashboard.html')
