from django.conf import settings
from  django.conf.urls.static import static
from django.urls import path
from .views import home, about, category, contact, detail, search

urlpatterns = [
    path('', home, name="home"),
    path('search/', search, name="search"),
    path('about/', about, name="about"),
    path('category/<slug:slug>/', category, name="category"),
    path('contact/', contact, name="contact"),
    path('post/<slug:slug>/', detail, name="detail"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)