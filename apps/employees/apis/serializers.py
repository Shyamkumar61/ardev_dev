from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Employee, EmployeeBank
from PIL import Image as PILImage
from apps.general.apis.serializers import ServiceSerializer, EmployeeDesignation, DesignationSerializer


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

    emp_bank = EmployeeBankIdSerializer(required=False, many=True)
    profile_img = serializers.ImageField(required=False, validators=[_image_format_validation])
    pcc_image = serializers.ImageField(required=False, validators=[_image_format_validation])
    aadhar_image = serializers.ImageField(required=False, validators=[_image_format_validation])
    bank_id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request'] if 'context' in kwargs and 'request' in kwargs['context'] else None
        if request and (request.method == "PUT" or request.method == "PATCH"):
            self.Meta.exclude = ('created', 'modified')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Employee
        exclude = ('created', 'modified')

    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise ValidationError("No Numbers Are Allowed")
        return value

    def validate_aadhar(self, value):
        if len(value) < 12:
            raise ValidationError("Please Enter the Correct Aadhar Number")
        elif value.isalpha():
            raise ValidationError("No Characters are Allowed")
        return value
    
    def validate(self, attrs):
        emp_id = attrs.get('emp_id')
        instance = self.instance
        if Employee.objects.exclude(pk=instance.pk).filter(emp_id=emp_id).exists():
            raise ValidationError({'error': "employee Id already Exixts"})
        return attrs
            
    def create(self, validated_data):
        bank_details = validated_data.pop('emp_bank', [])
        employee = Employee.objects.create(**validated_data)
        for bank_detail in bank_details:
            EmployeeBank.objects.create(employee=employee, **bank_detail)
        return employee

    def update(self, instance, validated_data):
        emp_bank_data = validated_data.pop('emp_bank', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for bank_data in emp_bank_data:
            account_number = bank_data['accountNumber']
            employee_bank, created = EmployeeBank.objects.get_or_create(employee=instance, bank=bank_data['bank'],
                                                                        accountNumber=account_number,
                                                                        ifscCode=bank_data['ifscCode'])
            if not created:
                for attr, value in bank_data.items():
                    setattr(employee_bank, attr, value)
            employee_bank.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['designation'] = {
            "id": instance.designation.pk,
            "name": instance.designation.name
        }
        response['current_company'] = {
            "id": instance.current_company.pk,
            "name": instance.current_company.client_name
        }
        return response


class EmployeeListSerializer(serializers.Serializer):

    name = serializers.CharField(read_only=True)
    emp_id = serializers.CharField(read_only=True)
    phone_no = serializers.CharField(read_only=True)
    designation = serializers.CharField(read_only=True)
    current_company = serializers.SlugRelatedField(read_only=True, slug_field='client_name')






