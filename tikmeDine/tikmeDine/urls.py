
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tikmeReservation.urls')),  # Include tikmeCustomer app URLs
    path('auth/', include('authentication.urls')),
    path('systemadmin/', admin.site.urls),
    path('admin/', include('tikmeAdmin.urls')),
    path('admin/', include('tikmeReservation.urls')),
]
