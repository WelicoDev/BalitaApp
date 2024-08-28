from django.contrib import admin
from django.urls import path ,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/panel/', admin.site.urls),
    path('', include('app.urls')),
    path('users/', include('users.urls'), name="users"),
]
urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)