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
        if(isinstance(formfield, forms.IntegerField)):
            formfield.widget.attrs['min'] = 0;
            formfield.widget.attrs['step'] = 1;
    return formfield

class BusinessApplicationForm(forms.ModelForm):
    formfield_callback = modify_attr
    class Meta:
        formfield_callback = modify_attr
        model = models.BusinessPermitApplication
        exclude = (
            'user', 
            'application_type', 
            'submission_timestamp',
            'application_timestamp',
            'submission_status',
            'application_status'
            ) 

    def save(self,commit=True, **kwargs):
        application = super().save(commit = False)
        application.user = kwargs.pop('user')
        application.application_type = kwargs.pop('application_type')
        if commit:
            application.save()
        return application


class BusinessActivityForm(forms.ModelForm):
    class Meta:
        model = models.BusinessActivity
        exclude = ('business_application',) 

    def save(self, commit=True, **kwargs):
        business_activity = super().save(commit = False)
        try:
            business_activity.business_application = kwargs.pop('business_application')
        except KeyError:
            business_activity.business_application = None
        if commit:
            business_activity.save()
        return business_activity


class RequirementsForm(forms.ModelForm):
    class Meta:
        model = models.Requirement
        fields ='__all__'

    def save(self, commit=True, **kwargs):
        requirement = super().save(commit = False)
        try:
            requirement.application = kwargs.pop('application')
        except KeyError:
            requirement.application = None
        if commit:
            requirement.save()
        return requirement