from django.shortcuts import redirect

def allowed_users(groups = []):
    if not isinstance(groups, list):
        raise ValueError('groups must be a list')
    def wrapper_view(view):
        def wrapper(request, *args, **kwargs):
            
            user = request.user
            print(groups, user.username)
            for group in user.groups.all():
                if group.name not in groups:
                    return redirect('system_auth:unauthorized')
                
            return view(request, *args, **kwargs)
                
        return wrapper 
    return wrapper_view

        