from rest_framework.views import Response, Request, HttpResponseBase
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, GenericAPIView
from rest_framework import status
from .serializers import RegisterUserSerializer, LoginSerializer
from apps.account.models import Account
from django.contrib.auth import authenticate
from apps.account.mixins import LoginMixin


class LoginAPIView(LoginMixin,
                   GenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.login(request, *args, **kwargs)


class RegisterUserView(CreateAPIView):

    queryset = Account.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "Account Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(LoginAPIView):

    serializer_class = LoginSerializer
    queryset = Account.objects.all()

    def post(self, request, *args, **kwargs):
        return super().login(request, *args, **kwargs)


# class SendPasswordResetEmailView(APIView):
#
#     def post(self, request):
#         email = request.data['email']
#         if email is not None:
#             serializer = ""

