"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Django Admin sarlavhalarini moslashtirish
admin.site.site_header = "Masuf Admin Paneli"
admin.site.site_title = "Masuf Naftalan Boshqaruvi"
admin.site.index_title = "Tizim Boshqaruvi va Ma'lumotlar Bazasi"

urlpatterns = [
    # 1. Django Standart Admin Paneli
    path('admin/', admin.site.urls),
    
    # 2. Landing Page va Custom Manager Dashboard
    path('', include('landing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
