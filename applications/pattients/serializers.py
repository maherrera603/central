from rest_framework import serializers
#models
from .models import Pattient, Family

class RegisterSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=70)
    password = serializers.CharField()
    
    def validate(self, data):
        password = data["password"]
        if len(password) < 8 or len(password) > 12:
            raise serializers.ValidationError("La Contraseña debe tener de 8 a 12 caracteres")
        return data
    
class UpdatedSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)

    read_only_fields = ['type_document', 'document']

    
    def validate_name(self, data):
        if len(data) <= 3 or len(data) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return data
    
    def validate_lastname(self, data):
        if len(data) <= 3 or len(data) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return data
    
class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        exclude =  ["created_at", "updated_at"]
        
class UpdateFamilySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)