from django.http import JsonResponse
from rest_framework import authentication, permissions

def login_required(view_func):
    print("ssss")
    def wrapper_func(request,*args, **kwargs):
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [permissions.IsAuthenticated]
        return view_func
    return wrapper_func

