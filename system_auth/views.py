from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages

from . import forms, models
# Create your views here.

User = get_user_model()


def signup_view(request):
    
    if request.GET.get('validation') == 'true':

        json = {}
        msg = '{} is already taken'
        name = request.GET.get('name')
        print(request.GET)
        if name == 'email':
            email_value = request.GET.get('value')
            json['name'] = name
            try:
                User.objects.get(email = email_value)
                json['taken'] = True
                json['msg'] = msg.format(name)
            except User.DoesNotExist:  
                json['taken'] = False
        if name == 'username':
            username_value = request.GET.get('value')
            json['name'] = name
            try:
                User.objects.get(username = username_value)
                json['taken'] = True
                json['msg'] = msg.format(name)
            except User.DoesNotExist:
                json["taken"] = False
        
        return JsonResponse(json)

    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
    
                messages.success(request, 'You may now login to your account')
                print('User saved %r' % (user,))
                return redirect('system_auth:sign-in')
                

    return render(request, 'system_auth/sign-up.html')





def signin_view(request):
    if request.method == 'POST':
        form = forms.AuthenticationForm(request, request.POST)

        response = None
        if form.is_valid():
            login(request, form.user)
            try:
                groups = form.user.groups.all()
            except Exception as e: 
                response = redirect('client:home') 
            else:
                group_names = [g.name for g in groups]
                if 'staffs' in group_names:
                    response = redirect('staff:home')
                
                else:
                    response = redirect('client:home') 
                
            return response
        else:
            messages.error(request, 'The email or username and password are incorrect. Try again')

    return render(request, 'system_auth/sign-in.html')


def logout_view(request):
    logout(request)
    return redirect('system_auth:sign-in')


def unauthorized(request):
    return render(request, 'system_auth/unauthorized.html')