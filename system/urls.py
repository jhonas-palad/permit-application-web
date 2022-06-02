
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system_auth.urls', namespace='system_auth')),
    path('client/', include('client.urls', namespace='client')),
    path('staff/', include('staff.urls', namespace='staff')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
