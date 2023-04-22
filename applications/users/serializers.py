from rest_framework import  serializers

#
from .models import Role


class SuperUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    def validate_password(self, password):
        if len(password) < 8 or len(password) > 12:
            raise serializers.ValidationError("La contraseña debe contener de 8 a 12 caracteres")
        return password


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('role', )
        
    def validate_role(self, data):
        if len(data) < 5:
            raise serializers.ValidationError("Rol debe contener 5 o mas caracteres")
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_password(self, data):
        if len(data) < 8 or len(data) > 12:
            raise serializers.ValidationError("La cotraseña debe contener de 8 a 12 caracteres")
        
        return data

