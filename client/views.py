from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.db.models import Count, Q



from datetime import datetime as dt
import os


from system_auth.decorators import allowed_users
from .models import BusinessPermitApplication as BPA, BusinessActivity, Requirement
from . import forms
from . import sample
from .templatetags import twelve_hour_format, date_format




User = get_user_model()
@login_required
@allowed_users(['applicants'])

def test_view(request):
    response = render(request,'client/test-view.html')
    if request.GET.get('remove_cookies') == 'true':
        response.delete_cookie('something')
    if request.method == 'POST':
        response = HttpResponseRedirect(reverse('client:test-redirect'))
        response.set_cookie('something', {'aaa': 1111, 'bbbb': 2222})
        # response.something = 'ADIK'
        return response

    return response
@login_required
@allowed_users(['applicants'])
def test_redirect(request):
    context = {}
    print(request.COOKIES['something'])
    a = eval(request.COOKIES['something'])
    print(a, type(a), type(request.COOKIES['something']))
        

    context['something'] = getattr(request, 'something', 'OHH SNAP')

    return render(request,'client/test-redirect.html', context)

@login_required
@allowed_users(['applicants'])
def home_view(request):
    user = request.user
    print(user.groups.all())
    permit_applications = BPA.objects.filter(
        Q(user = user),
        Q(submission_status = BPA.SUBMITTED) |
        Q(submission_status = BPA.VERIFIED) |
        Q(submission_status = BPA.DENIED)
    )

    aggr = BPA.objects.filter(user = user).aggregate(
        submitted = Count('pk', filter = Q(submission_status = BPA.SUBMITTED)),
        verified = Count('pk', filter = Q(submission_status = BPA.VERIFIED)),
        denied = Count('pk', filter = Q(submission_status = BPA.DENIED))
    )
    context = {}
    
    enum_applications = [(index + 1, obj) for index, obj in enumerate(permit_applications)]
    
    
    page_objects = Paginator(enum_applications, 5)
    
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
    context['client'] = True
    context['name'] = user.first_name
    context['new'] = 'new'
    context['PERMIT_APPLICATIONS'] = enum_applications
    context['page_objects'] = page_objects.get_page(1)
    context['count'] = permit_applications.count()
    context['PERMIT_AGGR'] = aggr

    return render(request, 'client/home-view.html', context)

@login_required
@allowed_users(['applicants'])
def upload_image(request):
    user = request.user
    data = {}
    if request.method == 'POST':
        print(request.POST)
        
        if request.POST.get('upload'):
            
            form = forms.RequirementsForm(data = request.POST, files = request.FILES)
            if form.is_valid():
                permit_application_pk = request.POST.get('permit_application_pk', None)

                if permit_application_pk is None:
                    permit_application_pk = request.COOKIES.get('permit_application').split(':')[0]
                
                    

                permit_application = BPA.objects.get(pk = permit_application_pk)
                image = form.save(application = permit_application)
                permit_application.add_to_cache(image.filename, image.pk)
                data['filename'] = image.filename
                data['image_pk'] = image.pk
                data['success'] = True
                print(permit_application.show_cache())
            else:

                data['success'] = False

                print(image.errors.__repr__())


        data['end_point'] = '/upload_image/'
        response = JsonResponse(data)
        
        return response

    return redirect('client:permit-application')


@login_required
@allowed_users(['applicants'])
def remove_image(request):
    user = request.user
    permit_application_pk = request.COOKIES.get('permit_application').split(':')[0]
    
    data = {}

    if request.method == 'POST':
        permit_application = BPA.objects.get(pk = permit_application_pk)
        print(request.POST)
        if request.POST.get('remove'):
            filename = request.POST.get('filename', None)
            if request.POST.get('file_pk'):
                file_pk = request.POST.get('file_pk')
            else:
                file_pk = permit_application.get_cache(filename)
            # print(user.get_cache('upload_cache'))
            
            file = Requirement.objects.get(pk = file_pk)
            print(file.filename)
            file.delete()
            permit_application.remove_from_cache(filename)
            data['success'] = True
            data['file_id'] = file_pk
        data['end_point'] = '/remove_image/'
        return JsonResponse(data)
    return redirect('client:permit-application')

@login_required
@allowed_users(['applicants'])
def add_business_line(request):
    user = request.user
    data = {}
    if permit_application_pk := request.COOKIES.get('permit_application').split(':')[0]:
        permit_application = BPA.objects.get(pk = permit_application_pk)
    if request.method == 'POST':
        print(request.POST, permit_application)
        business_act_form = forms.BusinessActivityForm(request.POST)
        if business_act_form.is_valid():
            business_act = business_act_form.save(business_application=permit_application)
            data['pk'] = business_act.pk
            data['code'] = business_act.code
            data['capital_investment'] = business_act.capital_investment
            data['business_line'] = business_act.business_line
            data['no_units'] = business_act.no_units
            data['essential'] = business_act.essential
            data['non_essential'] = business_act.non_essential

        else:
            print(business_act_form.errors.__repr__())
        return JsonResponse(data)

    return redirect('client:permit-application')



@login_required
@allowed_users(['applicants'])
def update_business_line(request):
    data = {}

    if request.method == 'POST':
        print(request.POST)
        business_act_pk = request.POST.get('pk')
        business_act = BusinessActivity.objects.get(pk = business_act_pk)
        for k, v in request.POST.items():
            if not k == 'pk' and not k == 'csrfmiddlewaretoken':
                setattr(business_act, k, v)
                data[k] = v
        data['pk'] = business_act_pk
        business_act.save()

        return JsonResponse(data)


def delete_business_line(request):
    data = {}

    if request.method == 'POST':
        print(request.POST)
        business_act_pk = request.POST.get('pk')
        BusinessActivity.objects.get(pk = business_act_pk).delete()
        data['success'] = True
        return JsonResponse(data)

@login_required
@allowed_users(['applicants'])
def get_name(request):
    user = request.user
    data = {}
    data['surname'] = user.last_name
    data['given_name'] = user.first_name
    return JsonResponse(data)


@login_required
@allowed_users(['applicants'])
def permit_application(request,pk):
    user = request.user

    context = {}

    if not pk == 'new':
        
        permit_application = BPA.objects.get(pk = pk)
        application_form = forms.BusinessApplicationForm(instance = permit_application)
    else:
        
        application_form = forms.BusinessApplicationForm()
    
    if request.method == 'POST':

            
        data = {k: v for k, v in request.POST.items()}
        if(not request.POST.get('business_type') == '3'):
            data['corporation_type'] = 1
        if not pk == 'new':
            application_form_data = forms.BusinessApplicationForm(data, instance = permit_application)
        else:
            application_form_data = forms.BusinessApplicationForm(data)

        if application_form_data.is_valid():

            permit_application = application_form_data.save(user=user, application_type='N')
            response = redirect('client:permit-operation-requirements')
            response.set_cookie('permit_application', '%s:%s' %(permit_application.pk, 'new'))
            return response
        else:
            print(application_form_data.errors.__repr__())
                
                


    business_information_registration = (

        application_form['business_name'],
        application_form['trade_name'],
        application_form['registration_number'],
        application_form['tax_id_number'],
    )
    contact_details = (
        application_form['tel_no'],
        application_form['mobile_no'],
        application_form['email_address'],
    )
    business_address = (
        application_form['house_bldg_no'],
        application_form['blgd_name'],
        application_form['block_no'],
        application_form['subdivision'],
        application_form['street'],
        application_form['barangay'],
        application_form['city'],
        application_form['province'],
        application_form['zip_code'],
    )

    owner_information = (
        application_form['surname'],
        application_form['given_name'],
        application_form['middle_name'],
    )
    business_check_boxes = (
        application_form['rented'],
        application_form['tax_incentives'],
    )
    business_operation = (
        application_form['tax_declaration'],
        application_form['property_ident_no'],
        application_form['capital_investment'],
        application_form['business_area'],
        application_form['total_floor_area'],
        
    )
    employee_count = (
        application_form['female_emp_count'],
        application_form['male_emp_count'],
        application_form['tanauan_emp_count'],
    )
    vehicle_count = (
        application_form['van_truck_count'],
        application_form['motorcycle_count'],
    )
    
    context['business_information_registration'] = business_information_registration 
    context['contact_details'] = contact_details
    context['business_address'] = business_address
    context['owner_information'] = owner_information
    
    context['business_check_boxes'] = business_check_boxes
    context['business_operation'] = business_operation
    context['employee_count'] = employee_count
    context['vehicle_count'] = vehicle_count
    context['owner_check_box'] = application_form['owned']


    context['application_form'] = application_form

    response = render(request, 'client/permit-application.html', context = context)
    
    
    return response


@login_required
@allowed_users(['applicants'])
def permit_operation_requirements(request):
    context = {}
    pk = request.COOKIES.get('permit_application').split(':')[0]
    permit_application = BPA.objects.get(pk = pk)

    uploaded_requirements = Requirement.objects.filter(application = permit_application)
    business_activities = BusinessActivity.objects.filter(business_application = permit_application)
    

    IND_BUSINESS_ACTIVITIES = [(index + 1, obj) for index, obj in enumerate(business_activities)]
    
    print(IND_BUSINESS_ACTIVITIES)

    REQUIREMENT_LIST = []

    REQUIREMENT_LIST.append('Barangay clearance/permit')
    REQUIREMENT_LIST.append('Valid ID')

    business_type = permit_application.business_type

    if business_type == '1':
        REQUIREMENT_LIST.append('Proof of Registration DTI')
    elif business_type == '2' or business_type == '3':
        REQUIREMENT_LIST.append('Proof of Registration SEC')
    elif business_type == '4':
        REQUIREMENT_LIST.append('Proof of Registration CDA')
    else:
        REQUIREMENT_LIST.append('Proof of Registration')

    rented = permit_application.rented
    
    if rented:
        REQUIREMENT_LIST.append('Contract of Lease')
    
    owned = permit_application.owned
    if owned:
        REQUIREMENT_LIST.append('Tax Declaration')

    
    context['uploaded_requirements'] = uploaded_requirements
    context['IND_BUSINESS_ACTIVITIES'] = IND_BUSINESS_ACTIVITIES
    context['requirements'] = REQUIREMENT_LIST
    context['previous_pk'] = pk
    
    
        
    return render(request, 'client/permit-operation-requirements.html', context)



    

@login_required
def permit_application_summary(request, pk):

    permit_application = BPA.objects.get(pk = pk)
    uploaded_requirements = Requirement.objects.filter(application = permit_application)
    business_activities = BusinessActivity.objects.filter(business_application = permit_application)
    
    if request.method == 'POST':
        if submitted:= request.POST.get('submit') == 'True':
            has_new_cookie = False
            try:
                has_new_cookie = request.COOKIES.get('permit_application').split(':')[1] == 'new'
            except AttributeError:
                if not permit_application.is_submitted:
                    permit_application.submit_form()
            else:
                if has_new_cookie and not permit_application.is_submitted:
                    permit_application.submit_form()
                    messages.success(request, 'Application submitted')

            response = redirect('client:home')
            if has_new_cookie:
                response.delete_cookie('permit_application')
            return response


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
        'user_type': 'applicant'
    }

    

    return render(request, 'client/summary.html',context)
