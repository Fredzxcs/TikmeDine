from django.urls import path
from . import views

urlpatterns = [
    path('', views.tikmeCustomer, name='tikmeCustomer'),  # Adminpage
 
]