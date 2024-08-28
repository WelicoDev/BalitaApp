from django.urls import path
from .views import home, category, views, about, contact

urlpatterns = [
    path('', home , name='home'),
    path('category/<slug:slug>/', category, name="category"),
    path('posts/<slug:slug>/', views, name="views"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact")
]