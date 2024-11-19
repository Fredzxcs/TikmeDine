from django.urls import path
from .views import (
    create_reservation
)


urlpatterns = [
    # Authentication

    path('create_reservation/', create_reservation, name='create_reservation'),
    
]