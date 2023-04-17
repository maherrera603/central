from rest_framework import  serializers
from rest_framework.authtoken.models import Token
#
from .models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_password(self, data):
        if len(data) < 8 or len(data) > 12:
            raise serializers.ValidationError('La cotraseña debe contener de 8 a 12 caracteres')
        
        return data
