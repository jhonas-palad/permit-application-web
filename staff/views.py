from django.shortcuts import render
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime as dt

from .models import BusinessPermit

from client.templatetags import twelve_hour_format, date_format

from system_auth.decorators import allowed_users
from client.models import BusinessPermitApplication as BPA,BusinessActivity, Requirement

@login_required
@allowed_users(['staffs'])
def home(request):
    context = {}
    permit_applications = BPA.objects.filter(
        Q(submission_status = BPA.SUBMITTED) |
        ~Q(submission_status = BPA.VERIFIED) |
        ~Q(submission_status = BPA.DENIED)
    )
    enum_applications = [(index + 1, obj) for index, obj in enumerate(permit_applications)]
    page_objects = Paginator(enum_applications, 8)
    if page:= request.GET.get('page'):
        
        objects = page_objects.get_page(page)
        json_resp = {}
        for i, ind_obj in enumerate(objects):
            index, obj = ind_obj
            json_resp[i] = {
                'index' : index,
                'pk': obj.pk,
                'name': obj.business_name,
                'submission_datetime': (date_format(obj.submission_timestamp), 
                                        twelve_hour_format(obj.submission_timestamp)),
                'status': (obj.submission_status, obj.submission_status.title()),
            }

        
        if has_prev:= objects.has_previous():
            
            json_resp['prev_page'] = objects.previous_page_number()
        if has_next:= objects.has_next():
            
            json_resp['next_page'] = objects.next_page_number()

        json_resp['len'] = len(objects)
        json_resp['has_prev'] = has_prev
        json_resp['has_next'] = has_next

        return JsonResponse(json_resp)
    context['page_objects'] = page_objects.get_page(1)
    context['request'] = request
    return render(request ,'staff/home.html', context)


def view_application(request, pk):
    permit_application = BPA.objects.get(pk = pk)
    uploaded_requirements = Requirement.objects.filter(application = permit_application)
    business_activities = BusinessActivity.objects.filter(business_application = permit_application)

    BUSINESS_TYPES = ('Sole Proprietorship', 'Proprietorship', 'Corporation', 'Cooperative')
    BUSINESS_TYPE = BUSINESS_TYPES[int(permit_application.business_type) - 1]
    TOTAL_EMP_COUNT = int(permit_application.male_emp_count) + int(permit_application.female_emp_count) + int(permit_application.tanauan_emp_count)
    TOTAL_VEHICLE_COUNT = int(permit_application.van_truck_count) + int(permit_application.motorcycle_count)
    context = {
        'permit_application' : permit_application,
        'uploaded_requirements': uploaded_requirements,
        'business_activities': business_activities,
        'business_types' : BUSINESS_TYPES,
        'business_type': BUSINESS_TYPE,
        'total_no_emp' : TOTAL_EMP_COUNT,
        'total_no_vehicle': TOTAL_VEHICLE_COUNT,
        'user_type': 'staff'
    }

    return render(request, 'client/summary.html',context)

@login_required
@allowed_users(['staffs'])
def generate_permit(request):
    json = {}
    if request.method == 'POST':
        print("ASDASDASD")
        print(request.POST)
        bpa_pk = request.POST.get('pk')
        
        permit_application = BPA.objects.get(pk = bpa_pk)
        permit_application.evaluate_form('verified')
        BusinessPermit.objects.create(bpa = permit_application, staff = request.user)
        json['status'] = permit_application.submission_status

    return JsonResponse(json)

@login_required
@allowed_users(['staffs'])
def deny_permit(request):
    json = {}
    if request.method == 'POST':
        bpa_pk = request.POST.get('pk')
        permit_application = BPA.objects.get(pk = bpa_pk)
        permit_application.evaluate_form('denied')
        BusinessPermit.objects.create(bpa = permit_application, staff = request.user)
        son['status'] = permit_application.submission_status
    return JsonResponse(json)
