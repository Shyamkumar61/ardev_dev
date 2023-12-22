from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Employee, EmployeeBank
from PIL import Image as PILImage
import re
from apps.general.apis.serializers import ServiceSerializer, EmployeeDesignation, DesignationSerializer
from django.templatetags.static import static


def _image_format_validation(attrs):
    if attrs is not None:
        try:
            image = PILImage.open(attrs)
            image_format = image.format.lower()
            if image_format not in ['png', 'jpge', 'jpg']:
                raise ValidationError({'error': f'Invalid image format for {image}. Only PNG and JPEG are allowed.'}) 
        except Exception as e:
            raise ValidationError({'error': f'Invalid image format for {image}'})
    elif attrs is None:
        return attrs


class EmployeeBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeBank
        fields = ('bank', 'accountNumber', 'ifscCode')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bank'] = instance.bank.bank_name
        return response


class EmployeeBankIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeBank
        fields = ('bank', 'accountNumber', 'ifscCode')


class EmployeeSerializer(serializers.ModelSerializer):

    emp_bank = EmployeeBankIdSerializer(required=False, many=True, read_only=True)
    profile_img = serializers.ImageField(required=False, validators=[_image_format_validation])
    pcc_image = serializers.ImageField(required=False, validators=[_image_format_validation])
    aadhar_image = serializers.ImageField(required=False, validators=[_image_format_validation])

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request'] if 'context' in kwargs and 'request' in kwargs['context'] else None
        if request and (request.method == "PUT" or request.method == "PATCH"):
            self.Meta.exclude = ('created', 'modified')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Employee
        exclude = ('created', 'modified')

    def validate_emp_id(self, value):
        if not value:
            raise serializers.ValidationError("Emp Id cannot be Empty")
        elif not re.match(r'[0-9]*$', value):
            raise serializers.ValidationError("Emp Id cannot be Character or Special Character")
        return value

    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError("No Numbers Are Allowed")
        return value

    def validate_phone_no(self, value):
        phone_number_pattern = re.compile(r'^\d{10}$')
        if not value:
            raise serializers.ValidationError("Client Phone Number Cannot be Empty")
        elif len(value) < 10 or len(value) > 10:
            raise serializers.ValidationError({"message": "Invalid phone number format. Please enter a 10-digit number."})
        elif not phone_number_pattern.match(value):
            raise serializers.ValidationError(
                {"message": "Phone Number cannot contain Alphabets or Special Charaters"})
        return value

    def validate_whatsappNum(self, value):
        phone_number_pattern = re.compile(r'^\d{10}$')
        if not value:
            raise serializers.ValidationError("Client Phone Number Cannot be Empty")
        elif len(value) < 10 or len(value) > 10:
            raise serializers.ValidationError({"message": "Invalid phone number format. Please enter a 10-digit number."})
        elif not phone_number_pattern.match(value):
            raise serializers.ValidationError(
                {"message": "Phone Number cannot contain Alphabets or Special Charaters"})
        return value

    def validate_aadhar(self, value):
        if len(value) < 12:
            raise ValidationError("Please Enter the Correct Aadhar Number")
        elif value.isalpha():
            raise ValidationError("No Characters are Allowed")
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("Address Field cannot be Empty")
        return value

    def validate_uanNumber(self, value):
        if not value:
            raise serializers.ValidationError("uanNumber Cannot be Empty")
        elif len(value) != 12:
            raise serializers.ValidationError("uanNumber Only Contains 12 Numbers")
        elif not re.match(r'[0-9]*$', value):
            raise serializers.ValidationError("UanNumber Cannot Contain Character or Special Charater")
        return value

    def validate(self, attrs):
        emp_id = attrs.get('emp_id')
        instance = self.instance
        if not instance:
            if Employee.objects.filter(emp_id=emp_id).exists():
                raise ValidationError({'error': "employee Id already Exixts"})
        return attrs
            
    # def create(self, validated_data):
    #     bank_details = validated_data.pop('emp_bank', [])
    #     employee = Employee.objects.create(**validated_data)
    #     for bank_detail in bank_details:
    #         EmployeeBank.objects.create(employee=employee, **bank_detail)
    #     return employee

    # def update(self, instance, validated_data):
    #     emp_bank_data = validated_data.pop('emp_bank', [])
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     for bank_data in emp_bank_data:
    #         account_number = bank_data['accountNumber']
    #         employee_bank, created = EmployeeBank.objects.get_or_create(employee=instance, bank=bank_data['bank'],
    #                                                                     accountNumber=account_number,
    #                                                                     ifscCode=bank_data['ifscCode'])
    #         if not created:
    #             for attr, value in bank_data.items():
    #                 setattr(employee_bank, attr, value)
    #         employee_bank.save()
    #     return instance

    def to_representation(self, instance):
        request = self.context.get('request', None)
        response = super().to_representation(instance)
        response['designation'] = {
            "id": instance.designation.pk,
            "name": instance.designation.name
        }
        response['current_company'] = {
            "id": instance.current_company.pk,
            "name": instance.current_company.client_name
        }
        media_url = request.build_absolute_uri(static('images/'))
        if instance.profile_img:
            response['profile_img'] = f"{media_url}{instance.profile_img.name}"
        if instance.pcc_image:
            response['pcc_image'] = f"{media_url}{instance.pcc_image.name}"
        if instance.aadhar_image:
            response['aadhar_image'] = f"{media_url}{instance.aadhar_image.name}"
        return response


class EmployeeListSerializer(serializers.Serializer):

    name = serializers.CharField(read_only=True)
    emp_id = serializers.CharField(read_only=True)
    phone_no = serializers.CharField(read_only=True)
    designation = serializers.CharField(read_only=True)
    current_company = serializers.SlugRelatedField(read_only=True, slug_field='client_name')
    profile_img = serializers.SerializerMethodField()

    def get_profile_img(self, obj):
        if obj.profile_img:
            media_url = self.context['request'].build_absolute_uri(static('images/'))
            return f"{media_url}{obj.profile_img.name}"
        return None


class EmployeeCompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('emp_id', 'name', 'phone_no', 'bloodGroup', 'joining_date', 'profile_img', 'designation')

    def to_representation(self, instance):
        request = self.context.get('request', None)
        represent = super().to_representation(instance)
        represent['designation'] = instance.designation.name
        if instance.profile_img:
            media_url = request.build_absolute_uri(static('images/'))
            represent['profile_img'] = f"{media_url}{instance.profile_img.name}"
        return represent


class EmployeeBankSerializer(serializers.ModelSerializer):

    def validate_employee(self, value):
        instance = self.instance
        if value and not instance and EmployeeBank.objects.filter(employee=value).exists():
            raise serializers.ValidationError("This Employee Already has Bank Assingned")
        return value

    def validate_accountNumber(self, value):
        if not value:
            raise serializers.ValidationError("Account Number Field Cannot be empty")
        if value and not re.match(r'^[0-9]{11,16}$', value):
            raise serializers.ValidationError("Account Number Cannot be String or Special Characters")
        return value

    def validate_ifscCode(self, value):
        if not value:
            raise serializers.ValidationError("Please Enter Bank Ifsc Code")
        if value and not re.match(r'^[a-zA-Z0-9]*$', value):
            raise serializers.ValidationError("Account Number Cannot be String or Special Characters")
        return value

    def validate(self, attrs):
        instance = self.instance
        acc_num = attrs.get('accountNumber')
        if not instance and EmployeeBank.objects.filter(accountNumber=acc_num).exists():
            raise serializers.ValidationError("Account Number Already Exists")
        return attrs

    class Meta:
        model = EmployeeBank
        fields = ('bank', 'employee', 'accountNumber', 'ifscCode')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bank'] = {"value": instance.bank.id, "label": instance.bank.bank_name}
        response['employee'] = instance.employee.name
        return response
