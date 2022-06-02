from django.urls import path
from . import views

app_name = 'system_auth'

urlpatterns = (
    path('sign-up', views.signup_view, name = 'sign-up'),
    path('sign-in', views.signin_view, name = 'sign-in'),
    path('logout', views.logout_view, name='logout'),
    path('unauthorized', views.unauthorized, name='unauthorized'),
)