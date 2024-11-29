from django.urls import path
from . import views
from travelling.urls import views as travel_views
from travelling import settings

urlpatterns = [
    path("", travel_views.home),    

    path('registration/', views.hotel_owner_registration, name='hotel_registration'),
    path('login/', views.hotel_owner_login, name='hotel_login'),

    path("contact_support", views.contact_support, name='contact_support')
]