from django.urls import path

from . import views
app_name = 'staff'


urlpatterns = (
    path('', views.home, name='home' ),
    path('view-application/<pk>', views.view_application, name='view-application'),
    path('generate-permit', views.generate_permit, name='generate-permit'),
    path('deny-permit', views.deny_permit, name='deny-permit'),

)