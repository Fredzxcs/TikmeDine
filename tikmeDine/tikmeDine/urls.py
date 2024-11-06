from django.contrib import admin
from django.urls import path, include

urlpatterns = [
<<<<<<< HEAD
    path('', include('tikmeReservation.urls')),  # API routes for tikmeReservation app
    path('api-auth/', include('authentication.urls')),  # API routes for authentication
    path('api-admin/', include('tikmeAdmin.urls')),  # API routes for authentication
    path('systemadmin/', admin.site.urls),  # Admin interface
=======
    path('', include('tikmeReservation.urls')),  # Include tikmeCustomer app URLs
    path('auth/', include('authentication.urls')),
    path('systemadmin/', admin.site.urls),
    path('admin/', include('tikmeAdmin.urls')),
    path('admin/', include('tikmeReservation.urls')),
>>>>>>> 32624d54abe0064c6fc4ff8e7d5dc0df463c0d3f
]
