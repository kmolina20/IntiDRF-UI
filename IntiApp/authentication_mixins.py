from IntiApp.authentication import ExpiringTokenAuthentication

from django.shortcuts import render

from rest_framework.authentication import get_authorization_header
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer



class Authentication(object):
    user = None
    
    def get_user(self,request):
        """
        Return:
            * user      : User Instance or 
            * message   : Error Message or 
            * None      : Corrup Token
        """
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return None            
        
            token_expire = ExpiringTokenAuthentication()
            user = token_expire.authenticate_credentials(token)
            
            if user != None:
                self.user = user
                return user
        
        return None
    
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_superuser):
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request,'405.html') 