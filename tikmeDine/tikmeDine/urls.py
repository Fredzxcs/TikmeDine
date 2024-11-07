from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tikmeReservation.urls')),  # API routes for tikmeReservation app
    path('api-auth/', include('authentication.urls')),  # API routes for authentication
    path('api-admin/', include('tikmeAdmin.urls')),  # API routes for authentication
    path('systemadmin/', admin.site.urls),  # Admin interface
]
