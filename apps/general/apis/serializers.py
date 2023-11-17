from rest_framework import serializers
from apps.general.models import Services, Designation, Banks
from rest_framework.exceptions import ValidationError


def validate_name(value):
    if not isinstance(value, str):
        raise ValidationError("No Numbers are Allowed")
    return value


class ServiceOptionSerializer(serializers.Serializer):

    id = serializers.PrimaryKeyRelatedField(source='pk', read_only=True)
    value = serializers.CharField(source='service_name', read_only=True)


class ServiceSerializer(serializers.Serializer):

    id = serializers.PrimaryKeyRelatedField(source='pk', read_only=True)
    service_name = serializers.CharField(max_length=20, required=True, validators=[validate_name])
    is_active = serializers.BooleanField(default=True)

    def validate(self, data):
        service_name = data.get('service_name')
        if Services.objects.filter(service_name=service_name).exists():
            raise ValidationError("Service Already Exists")
        return data

    def create(self, validated_data):
        service = Services.objects.create(service_name=validated_data['service_name'])
        return service

    def update(self, instance, validated_data):
        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.save()
        return instance


class DesignationSerializer(serializers.Serializer):

    service = serializers.PrimaryKeyRelatedField(queryset=Services.objects.only('id'))
    name = serializers.CharField(max_length=20, required=True, validators=[validate_name])
    is_active = serializers.BooleanField(default=True)

    def validate(self, attrs):
        name = attrs.get('name')
        if Designation.objects.filter(name=name).exists():
            raise ValidationError("Designation Already Exists")
        return attrs

    def create(self, validated_data):
        try:
            service = Services.objects.get(id=validated_data['service'].id)
            designation = Designation.objects.create(service=service.id, name=validated_data['name'])
            return designation
        except Exception as e:
            raise ValidationError({"success": False, "data": str(e)})

    def update(self, instance, validated_data):
        try:
            service = Services.objects.get(id=validated_data['service'].id)
            instance.service = service
            instance.name = validated_data['name']
            instance.save()
            return instance
        except Exception as e:
            raise ValidationError({"success": False, "data": str(e)})

    def to_representation(self, instance):
        respresent = super().to_representation(instance)
        respresent['service'] = instance.service.service_name
        return respresent


class EmployeeDesignation(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ['id', 'name']

