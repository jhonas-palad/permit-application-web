from django.urls import path

from . import views

app_name = 'client'

urlpatterns = [
    path('', views.home_view, name ='home'),
    path('permit-application/<str:pk>', views.permit_application, name='permit-application'),
    path('permit-application/new/get-name', views.get_name, name='get-name'),
    path('permit-application/summary/<str:pk>', views.permit_application_summary, name='permit-application-summary'),
    path('permit-operation-requirements', views.permit_operation_requirements, name='permit-operation-requirements'),
    path('permit-operation-requirements/upload-image', views.upload_image, name='upload-image'),
    path('permit-operation-requirements/remove-image', views.remove_image, name='remove-image'),
    path('permit-operation-requirements/add-business-line', views.add_business_line, name='add-business-line'),
    path('permit-operation-requirements/update-business-line', views.update_business_line, name='update-business-line'),
    path('permit-operation-requirements/delete-business-line', views.delete_business_line, name='delete-business-line'),
    path('test-view', views.test_view, name='test-view'),
    path('test-redirect', views.test_redirect, name='test-redirect'),
]