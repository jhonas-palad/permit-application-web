from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from . import forms


User = get_user_model()



@login_required
def home_view(request, pk):
    user = User.objects.get(pk=pk)
    context = {}
    context['pk'] = pk
    return render(request, 'client-application/home-view.html', context)


@login_required
def permit_application(request, pk):
    context = {}
    application_form = forms.BusinessApplicationForm()
    # activity_form = forms.BusinessActivityForm()
    # requirements_form = forms.RequirementsForm()
    
    if request.method == 'POST':
        form = forms.BusinessApplicationForm(request.POST)
        if form.is_valid(): 
            form.save()

        if request.POST.get('fileuploading'):
            print(request.POST)
            print(request.FILES)
            
        
            return JsonResponse({'sucess': True})
        print(request.POST)
        print(request.FILES)

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
        application_form['lot_no'],
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
        application_form['owned'],
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



    context['pk'] = pk
    context['business_information_registration'] = business_information_registration 
    context['contact_details'] = contact_details
    context['business_address'] = business_address
    context['owner_information'] = owner_information
    context['business_check_boxes'] = business_check_boxes
    context['business_operation'] = business_operation
    context['employee_count'] = employee_count
    context['vehicle_count'] = vehicle_count


    context['application_form'] = application_form


    
    return render(request, 'client-application/permit-application.html', context = context)


# 'application_type': application_form['application_type'],
# 'business_name':application_form['business_name'],
# 'trade_name':application_form['trade_name'],
# 'business_type':application_form['business_type'],
# 'corporation_type':application_form['corporation_type'],
# 'registration_number':application_form['registration_number'],
# 'tax_id_number':application_form['tax_id_number'],
# 'tel_no':application_form['tel_no'],
# 'mobile_no':application_form['mobile_no'],
# 'email_address':application_form['email_address'],
# 'house_bldg_no':application_form['house_bldg_no'],
# 'blgd_name':application_form['blgd_name'],
# 'block_no':application_form['block_no'],
# 'lot_no':application_form['lot_no'],
# 'street':application_form['street'],
# 'barangay':application_form['barangay'],
# 'city':application_form['city'],
# 'province':application_form['province'],
# 'zip_code':application_form['zip_code'],
# 'surname':application_form['surname'],
# 'given_name':application_form['given_name'],
# 'middle_name':application_form['middle_name'],
# 'sex':application_form['sex'],
# 'owned':application_form['owned'],
# 'rented':application_form['rented'],
# 'tax_declaration':application_form['tax_declaration'],
# 'property_ident_no':application_form['property_ident_no'],
# 'capital_investment':application_form['capital_investment'],
# 'tax_incentives':application_form['tax_incentives'],
# 'business_area':application_form['business_area'],
# 'total_floor_area':application_form['total_floor_area'],
# 'female_emp_count':application_form['female_emp_count'],
# 'male_emp_count':application_form['male_emp_count'],
# 'tanauan_emp_count':application_form['tanauan_emp_count'],
# 'van_truck_count':application_form['van_truck_count'],
# 'motorcycle_count':application_form['motorcycle_count'],

# 'business_line':activity_form['business_line'],
# 'units':activity_form['units'],
# 'capital_investment':activity_form['capital_investment'],
# 'essential':activity_form['essential'],
# 'non_essential':activity_form['non_essential'],

# 'community_tax_certif':requirements_form['community_tax_certif'],
# 'barangay_clearance':requirements_form['barangay_clearance'],
# 'certification':requirements_form['certification'],
# 'zoning_certif':requirements_form['zoning_certif'],
# 'business_loc_sketch':requirements_form['business_loc_sketch'],
# 'lease_contract':requirements_form['lease_contract'],
# 'tax_declaration':requirements_form['tax_declaration'],



    # business_activity = (
    #     activity_form['business_line'],
    #     activity_form['units'],
    #     activity_form['capital_investment'],
    #     activity_form['essential'],
    #     activity_form['non_essential'],
    # )

    # business_requirement = (
    #     requirements_form['community_tax_certif'],
    #     requirements_form['barangay_clearance'],
    #     requirements_form['certification'],
    #     requirements_form['zoning_certif'],
    #     requirements_form['business_loc_sketch'],
    #     requirements_form['lease_contract'],
    #     requirements_form['tax_declaration'],
    # )