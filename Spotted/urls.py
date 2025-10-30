from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import go_to_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mod/', include('mods.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('accounts/profile/', go_to_home, name='profile'),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
