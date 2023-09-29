from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.account.models import Account
from rest_framework.exceptions import ValidationError
from apps.account.utils import generate_user

User = get_user_model()


def validate_name(value):
    if value and not value.isalpha():
        raise ValidationError("No Numbers are Allowed")
    return value


class RegisterUserSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=30, required=True,
                                   style={
                                       'input_type': 'text',
                                       'placeholder': 'Last Name',
                                   })
    first_name = serializers.CharField(max_length=20, required=True, validators=[validate_name],
                                       style={
                                           'input_type': 'text',
                                           'placeholder': 'Last Name',
                                       })
    last_name = serializers.CharField(max_length=20, required=True, validators=[validate_name],
                                      style={
                                          'input_type': 'text',
                                          'placeholder': 'Last Name',
                                      })
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password',
            'placeholder': 'Enter your password',
            'class': 'custom-password-field',
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            'input_type': 'password',
            'placeholder': 'Enter your password',
            'class': 'custom-password-field',
        }
    )

    def validate(self, attrs):
        email = attrs.get('email')
        if email and Account.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists")

        for field_name, field_value in attrs.items():
            if field_value is None:
                raise ValidationError(f"{field_name} is required")

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = Account.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=generate_user()
        )
        user.set_password(validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=30, required=True,
                                   style={
                                       'input_type': 'text',
                                       'placeholder': 'Last Name',
                                   })
    password = serializers.CharField(max_length=30, required=True,
                                     style={
                                        'input_type': 'password',
                                        'placeholder': 'Enter your password',
                                        'class': 'custom-password-field',
                                     })
