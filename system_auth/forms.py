from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from . import models


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(max_length=128)
    confirm_pass = forms.CharField(max_length=128)

    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email'

        )

    
    def clean_confirm_pass(self):
        password1 = self.cleaned_data.get("password")
        confirm_pass = self.cleaned_data.get("confirm_pass")
        if password1 and confirm_pass and password1 != confirm_pass:
            raise ValidationError()
        return password1

    def save(self, commit = True):
        user = super().save(commit = False)
        applicant_group = Group.objects.get(name='applicants')
        
        
       
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        applicant_group.user_set.add(user)
        applicant_group.save()
        return user

class AuthenticationForm(forms.Form):
    email_user = forms.CharField(max_length=128)
    password_login = forms.CharField(max_length=128)

    def __init__(self, request, *args,**kwargs):
        
        self.request = request
        self.user = None
        super().__init__(*args,**kwargs)

    
    def clean(self):
        email_user = self.cleaned_data['email_user']
        password_login = self.cleaned_data['password_login']

        if email_user and password_login:
            self.user = authenticate(self.request, username = email_user, password = password_login)
            print(self.user)
            if not self.user:
                raise ValidationError(
                    'Password incorrect',
                    code="password_incorrect")

        return self.cleaned_data
    


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ('user',)
