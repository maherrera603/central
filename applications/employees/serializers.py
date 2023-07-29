from rest_framework import serializers

# models
from .models import Employee

# serializers
from applications.users.serializers import UserResponseSerializer
from applications.users.serializers import UserSerializer


class EmployeeResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(write_only=False)
    document = serializers.CharField(write_only=False)
    
    class Meta:
        model = Employee
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "user"]


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=False)
    
    class Meta:
        model = Employee
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "user"]
    

    
class UpdatedEmployeeSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField()
    type_document = serializers.CharField()
    document = serializers.CharField()
    phone = serializers.CharField()
    
    def validate_name(self, name):
        if len(name) < 3 or len(name) > 20:
            raise serializers.ValidationError("el nombre debe contener de 3 a 20 caracteres")
        return name
    
    def validate_lastname(self, lastname):
        if len(lastname) < 3 or len(lastname) > 20:
            raise serializers.ValidationError("el apellido debe contener de 3 a 20 caracteres")
        return lastname
    
    def validate_phone(self, phone):
        if len(phone) < 10 or len(phone) > 10:
            raise serializers.ValidationError("el telefono debe contener 10 caracteres") 
        return phone
    
    

class EmployeeSearchSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Employee
        exclude =  ["created_at", "updated_at", "id_user"]
        