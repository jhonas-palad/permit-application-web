from django.db import models
from django.contrib.auth import get_user_model

from datetime import datetime as dt



class Cache:
    def __init__(self):
        self.cache = {}

    def __get__(self, obj, cls):
        if obj is None:
            return self
        
        try:
            cache = self.cache[obj]
        except KeyError:
            self.__set__(obj)
        else:
            return cache

        return self.cache[obj]

    def __set__(self, obj, value = {}):
        self.cache[obj] = value

class TableCache(Cache):
    pass

class UploadCache(Cache):
    pass

User = get_user_model()
# Create your models here.

class Requirement(models.Model):
    # community_tax_certif = models.ImageField('Community Tax Certificate',upload_to='ctc-certification')
    # barangay_clearance = models.ImageField('Barangay Clearance',upload_to='barangay-clearance')
    # certification = models.ImageField(upload_to='certification')
    # zoning_certif = models.ImageField(upload_to='zoning-certification')
    # business_loc_sketch = models.ImageField(upload_to='business-loc-sketch')
    # lease_contract = models.ImageField(upload_to='lease-contract', blank=True, null=True)
    # tax_declaration = models.ImageField(upload_to = 'tax-declaration', blank=True, null=True)
    filename = models.CharField(max_length = 255)
    requirement = models.ImageField(upload_to='requirements/')
    application = models.ForeignKey('BusinessPermitApplication',null = True,blank = True,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.filename} {self.requirement} {self.application}"
        
    def delete(self, *args, **kwargs):
        self.requirement.delete()
        super().delete(*args, **kwargs)
        
    def get_path(self):
        return self.requirement

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
    VERIFIED = 'verified'
    DENIED = 'denied'
    SUBMITTED = 'submitted'
    
    SUBMISSION_STATUS = (
        ('VERIFIED', 'Verified'),
        ('DENIED', 'Denied'),
        ('SUBMITTED', 'Submitted')
        
    )
    APPLICATION_STATUS = (
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    )
    submission_status = models.CharField(null = True, 
                                         max_length = 20, 
                                         blank = True, 
                                         choices = SUBMISSION_STATUS
                                         )
    application_status = models.CharField(null = True, 
                                          max_length = 20, 
                                          blank = True, 
                                          choices = APPLICATION_STATUS
                                          )
    submission_timestamp = models.DateTimeField(null=True)
    application_timestamp = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=2, choices=APPLICATION_TYPE)
    #Business information and registration
    business_name = models.CharField('Business Name',max_length=255)
    trade_name = models.CharField('Trade/Franchise Name',max_length = 255, null=True)
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
    block_no = models.CharField('Block No.', max_length = 50,blank = True,null=True)
    subdivision = models.CharField('Subdivision.', max_length = 100,blank = True, null=True)
    street = models.CharField('Street', max_length = 50,blank = True, null=True)
    barangay = models.CharField('Barangay', max_length = 100)
    city = models.CharField('City', max_length = 100, default = 'Tanauan City')
    province = models.CharField('Province', max_length = 100, default = 'Batangas')
    zip_code = models.CharField('Zip Code', max_length = 100, default = '4232')

    #Owner Information
    
    surname = models.CharField('Surname', max_length = 255)
    given_name = models.CharField('Given Name', max_length = 255)
    middle_name = models.CharField('Middle Name', max_length = 255, null=True)
    sex = models.CharField('Sex', max_length = 1, choices = SEX)

    #Business Operation
    owned = models.BooleanField('I am the business owner',default=False)
    rented = models.BooleanField('The business rents a property',default=False)
    tax_declaration = models.CharField('Tax Declaration', max_length = 100)
    property_ident_no = models.CharField('Property Identification No.', max_length = 100)
    capital_investment = models.FloatField('Paid up Capital + Lease Expenses + Equipments', default = 0.0)
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
    class Meta:
        ordering = ['-submission_timestamp']
    upload_cache = UploadCache()
    def add_to_cache(self, filename, pk):

        cache = self.upload_cache
        cache[filename] = pk
    def show_cache(self):
        cache = self.upload_cache
        return cache

    def get_cache(self, filename):
        pk = self.upload_cache.get(filename, None)
        return pk
    
    @property
    def is_submitted(self):
        return self.submission_status == 'submitted'
    
    @property
    def is_verified(self):
        return self.submission_status == 'verified'
    
    @property
    def is_denied(self):
        return self.submission_status == 'denied'

    def submit_form(self):
        date_now = dt.now()
        self.submission_status = 'submitted'
        self.submission_timestamp = date_now
        self.save()
    
    def evaluate_form(self, evaluation = 'verified'):
        date_now = dt.now()
        self.submission_status = evaluation
        self.submission_timestamp = date_now
        self.save()



    def remove_from_cache(self,filename):
        
        cache = self.upload_cache
        if filename in cache:
            del cache[filename]


class BusinessActivity(models.Model):

    business_application = models.ForeignKey(BusinessPermitApplication, null = True, blank = True,on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    business_line = models.CharField(max_length=255)
    no_units = models.IntegerField()
    capital_investment = models.FloatField()
    essential = models.FloatField()
    non_essential = models.FloatField()




   


    

