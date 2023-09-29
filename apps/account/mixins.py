from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.contrib.auth import authenticate
from apps.account.utils import get_token_for_user


class LoginMixin:

    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_cred = self.perform_login(serializer)
        if user_cred is not None:
            response = Response({"success": user_cred}, status=status.HTTP_200_OK)
            response.set_cookie('auth_token', user_cred['token'])
            return response
        return Response({'error': "Invalid UserCredential"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_login(self, serializer):
        user = authenticate(request=None,
                            email=serializer.data['email'],
                            password=serializer.data['password'])
        if user is not None:
            token = get_token_for_user(user)
            return {
                        'token': token,
                        'msg': 'Login Success',
                        'User Id': user.id,
                        'Username': user.username,
                        'name': user.first_name + " " + user.last_name
                }
        return None





