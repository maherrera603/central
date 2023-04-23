from rest_framework import serializers

# models 
from .models import Cites


class RegisterCiteSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField()
    type_document = serializers.CharField()
    document = serializers.CharField()
    phone = serializers.CharField()
    eps = serializers.CharField()
    speciality = serializers.CharField()
    status = serializers.CharField()
    
    def validate_name(self, name):
        if len(name) < 3 or len(name) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return name
    
    def validate_lastname(self, lastname):
        if len(lastname) < 3 or len(lastname) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return lastname 
    
    
    def validate_phone(self, phone):
        if len(phone) < 10 or len(phone) > 10:
            raise serializers.ValidationError("el campo debe contener 10 caracteres")
        return phone 
    
    def validate_eps(self, eps):
        if len(eps) < 3 or len(eps) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return eps 
    
    def validate_speciality(self, speciality):
        if len(speciality) < 3 or len(speciality) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return speciality 
    
    def validate_status(self, status):
        if len(status) < 3 or len(status) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return status 
    
    