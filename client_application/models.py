from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Requirements(models.Model):
    # community_tax_certif = models.ImageField('Community Tax Certificate',upload_to='ctc-certification')
    # barangay_clearance = models.ImageField('Barangay Clearance',upload_to='barangay-clearance')
    # certification = models.ImageField(upload_to='certification')
    # zoning_certif = models.ImageField(upload_to='zoning-certification')
    # business_loc_sketch = models.ImageField(upload_to='business-loc-sketch')
    # lease_contract = models.ImageField(upload_to='lease-contract', blank=True, null=True)
    # tax_declaration = models.ImageField(upload_to = 'tax-declaration', blank=True, null=True)
    
    requirement = models.ImageField(upload_to='requirements/')
    application = models.ForeignKey('BusinessPermitApplication', on_delete=models.CASCADE)

class BusinessPermitApplication(models.Model):
    APPLICATION_TYPE = (
        ('N', 'New'),
        ('RN', 'Renew')
    )
    BUSINESS_TYPE = (
        ('1', 'Sole Proprietorship'),
        ('2', 'Partnership'),
        ('3', 'Corporation'),
        ('4', 'Cooperative'),
    )
    SEX = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    CORPORATION = (
        ('1', 'Filipino'),
        ('2', 'Foreign')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=2, choices=APPLICATION_TYPE)
    #Business information and registration
    business_name = models.CharField('Business Name',max_length=255)
    trade_name = models.CharField('Trade/Franchise Name',max_length = 255, null=True, blank=True)
    business_type = models.CharField('Type of business',max_length = 1, choices = BUSINESS_TYPE, default='1')
    corporation_type = models.CharField('For Corporation',max_length=1, choices = CORPORATION, default='1')
    registration_number = models.CharField('DTI/SEC/CDA Registration Number',max_length = 128)
    tax_id_number = models.CharField('Tax Identification Number', max_length = 128)
    tel_no = models.CharField('Tel No.', max_length = 20)
    mobile_no = models.CharField('Mobile No.', max_length = 20)
    email_address = models.CharField('Email Address', max_length = 255)

     #Business Address
    house_bldg_no = models.CharField('House/Bldg No.', max_length = 50)
    blgd_name = models.CharField('Building Name', max_length = 255)
    block_no = models.CharField('Block No.', max_length = 50, blank=True, null=True)
    lot_no = models.CharField('Lot No.', max_length = 50, blank=True, null=True)
    street = models.CharField('Street', max_length = 50, blank=True, null=True)
    barangay = models.CharField('Barangay', max_length = 100)
    city = models.CharField('City', max_length = 100, default = 'Tanauan City')
    province = models.CharField('Province', max_length = 100, default = 'Batangas')
    zip_code = models.CharField('Zip Code', max_length = 100, default = '4232')

    #Owner Information
    
    surname = models.CharField('Surname', max_length = 255)
    given_name = models.CharField('Given Name', max_length = 255)
    middle_name = models.CharField('Middle Name', max_length = 255, blank=True, null=True)
    sex = models.CharField('Sex', max_length = 1, choices = SEX)

    #Business Operation
    owned = models.BooleanField('I am the business owner',default=True)
    rented = models.BooleanField('The business rents a property',default=False)
    tax_declaration = models.CharField('Tax Declaration', max_length = 100)
    property_ident_no = models.CharField('Property Identification No.', max_length = 100)
    capital_investment = models.FloatField('Paid up Capital + Lease Expenses + Equipments')
    tax_incentives = models.BooleanField('Tax incentives from government entity', default=False)
    business_area = models.CharField('Business Area(in sq. m)', max_length=100)
    total_floor_area = models.CharField('Total Floor Area (in sq.m.)', max_length=100)
    female_emp_count = models.IntegerField('Female', default=0)
    male_emp_count = models.IntegerField('Male', default = 0)
    tanauan_emp_count = models.IntegerField('Residing within Tanauan City', default=0)
    van_truck_count = models.IntegerField('Van/Truck', default = 0)
    motorcycle_count = models.IntegerField('Motorcycle', default = 0)

    #Business Activity
    #Business Requirements



# class BusinessActivity(models.Model):

#     business_application = models.ForeignKey(BusinessPermitApplication, on_delete=models.CASCADE)
#     business_line = models.CharField(max_length=255)
#     units = models.IntegerField()
#     capital_investment = models.FloatField()
#     essential = models.FloatField()
#     non_essential = models.FloatField()




   


    

