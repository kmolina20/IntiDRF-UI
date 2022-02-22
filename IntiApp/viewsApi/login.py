from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from IntiApp.authentication_mixins import Authentication



class UserToken(Authentication, APIView):
    """
    Validate Token
    """
    def get(self,request,*args,**kwargs):        
        try:
            user_token = Token.objects.get(user = self.user)
            return Response({
                'token': user_token.key
            })
        except:
            return Response({
                'error': 'Bad submitted credentials'
            },status = status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):

    def post(self,request,*args,**kwargs):
        # send to serializer username and password
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                #user_serializer = UserTokenSerializer(user)
                if created:   
                    return Response({
                        'token': token.key,
                        'message': 'Login Successful'
                    }, status = status.HTTP_201_CREATED)
                else:
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'message': 'Login Successful'
                    }, status = status.HTTP_201_CREATED)
            else:
                return Response({'error':'This User cannot log in'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Username or password incorrect'}, status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):

    def get(self,request,*args,**kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()

            if token:
                user = token.user
                # delete all sessions for user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        # search auth_user_id, this field is primary_key's user on the session
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                # delete user token
                token.delete()
                
                session_message = 'Deleted User sessions'  
                token_message = 'Token removed'
                return Response({'token_message': token_message,'session_message':session_message},
                                    status = status.HTTP_200_OK)
            
            return Response({'error':'A User with these credentials was not found'},
                    status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Token not found in request'}, 
                                    status = status.HTTP_409_CONFLICT)