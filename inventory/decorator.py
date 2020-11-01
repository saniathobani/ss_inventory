from django.http import HttpResponse
from django.shortcuts import redirect, render

def allowed_users(allow=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allow:    
                return view_func(request, *args, **kwargs)
            else:
                return render(request,'login.html')
        return wrapper
    return decorator

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.groups.user.all()[0].name
        if group is 'admin':    
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized")
    return wrapper