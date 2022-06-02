from django import forms
from . import models

def modify_attr(field, **kwargs):
    
    formfield = field.formfield(**kwargs)
    if(not field.primary_key):
        if(isinstance(formfield, forms.CharField) or 
        isinstance(formfield, forms.IntegerField) or 
        isinstance(formfield, forms.FloatField)):
            formfield.widget.attrs['value'] = ''
            formfield.widget.attrs['onkeyup'] = "this.setAttribute('value',this.value);"

    return formfield

class BusinessApplicationForm(forms.ModelForm):
    formfield_callback = modify_attr
    class Meta:
        formfield_callback = modify_attr
        model = models.BusinessPermitApplication
        exclude = ('user', 'requirements') 


# class BusinessActivityForm(forms.ModelForm):
#     class Meta:
#         model = models.BusinessActivity
#         exclude = ('business_application',) 


# class RequirementsForm(forms.ModelForm):
#     class Meta:
#         model = models.Requirements
#         fields ='__all__'