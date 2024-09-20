
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('menu/', views.menu, name='menu'),  # Menu page
    path('reservation/', views.reservation, name='reservation'),  # Menu page
    path('faq/', views.faq, name='faq'),  # Menu page
    path('contact/', views.contact, name='contact'),  # Menu page
]
