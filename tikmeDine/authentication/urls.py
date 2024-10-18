from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminAuthentication, name='adminAuthentication'),  # Authentication page
]

urlpatterns = [
    path('', views.adminPortal, name='adminPortal'),  # Portal page
]