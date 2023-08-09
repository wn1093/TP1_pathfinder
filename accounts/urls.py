from  django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('contact', views.contact, name='contact'),
    path('contact_airline', views.contactAirline, name='contact_airline'),
    path('about', views.about, name='about'),
    path('news', views.news, name='home_search_form'),
    path('destinations', views.destinations, name='destinations'),
]