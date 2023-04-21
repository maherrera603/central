from rest_framework import serializers
# models
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField(max_length=1)
    
    class Meta:
        model = Employee
        exclude =  ['created_at', 'updated_at']
        
    def validate_password(self, password):
        if len(password) < 8 or len(password) > 12:
            raise serializers.ValidationError('la contraseña debe contener de 8 a 12 caracteres')
        return password
    
    
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