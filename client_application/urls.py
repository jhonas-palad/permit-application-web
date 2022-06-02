from django.urls import path

from . import views

app_name = 'client_application'

urlpatterns = [
    path('home/<pk>', views.home_view, name ='home'),
    path('permit-application/<pk>', views.permit_application, name='permit-application'),
]