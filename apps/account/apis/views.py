from rest_framework.views import Response, APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterUserSerializer, LoginSerializer
from apps.account.models import Account, LoginHistory
from django.contrib.auth import authenticate
from apps.account.mixins import LoginMixin, get_client_ip
from apps.account.signals import user_token_logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes


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



@permission_classes([AllowAny])
class LoginView(LoginAPIView):

    serializer_class = LoginSerializer
    queryset = Account.objects.all()

    def post(self, request, *args, **kwargs):
        return super().login(request, *args, **kwargs)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            if request.user.is_authenticated and isinstance(request.user, Account):
                user_token_logout.send(sender=request.user.__class__, user=request.user, request=request)
                response = Response({"success": True, "data": "User Logout Successfull"}, status.HTTP_200_OK)
                response.delete_cookie('auth_token')
                return response
            else:
                return Response({"success": False, "error": "User is not authenticated"},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)