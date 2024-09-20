# tikmeReservations/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tikmeReservation.urls')),  # Include tikmeCustomer app URLs
    # You can also include tikmeAdmin URLs if needed
]
