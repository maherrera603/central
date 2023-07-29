from rest_framework import serializers

# models
from .models import Status
from .models import Speciality
from .models import Doctor
from applications.employees.models import Employee

# serializers
from applications.employees.serializers import EmployeeResponseSerializer


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "last_name", "phone"]


class StatusResponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=False)
    status = serializers.CharField(read_only=False, required=False, allow_blank=True)
    
    class Meta:
        model = Status
        fields = ["id", "status"]


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    
    def validate_status(self, status):
        if len(status) < 3 or len(status) > 20:
            raise serializers.ValidationError("El estado debe contener de 3 a 20 caracteres")
        return status


class SpecialityResponseSerializer(serializers.ModelSerializer):
    employee = EmployeeResponseSerializer(write_only=False)
    speciality = serializers.CharField(write_only=False)
    
    class Meta:
        model = Speciality
        fields = ["id", "speciality", "employee"]


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ["id", "speciality"]
    
    
class DoctorResponseSerializer(serializers.ModelSerializer):
    speciality = SpecialityResponseSerializer(write_only=False)
    status = StatusResponseSerializer(write_only=False)
    employee = EmployeeResponseSerializer(write_only=False)
    
    class Meta:
        model = Doctor
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "speciality", "status", "employee"]
  
    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "speciality", "status"]
        
        
class DoctorSerializer(serializers.ModelSerializer):
    document = serializers.CharField(write_only=False)
    class Meta:
        model = Doctor
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "speciality", "status"]