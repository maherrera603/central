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