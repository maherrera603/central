from rest_framework import serializers

#models
from .models import Pattient
from .models import Family

# serializers
from applications.users.serializers import UserResponseSerializer


class PattientResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer()
    class Meta:
            model = Pattient
            fields = ["id", "name", "last_name", "type_document", "document", "phone", "user"]

class RegisterSerilizer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length=12)
    
    class Meta:
        model = Pattient
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "email", "password"]
    
    def validate_name(self, data):
        if len(data) <= 3 or len(data) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return data
    
    
class UpdatedSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)
    eps = serializers.CharField(max_length=50)
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
        exclude =  ["id_pattient" ,"created_at", "updated_at"]
    
        
class UpdateFamilySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)
    eps = serializers.CharField(max_length=50)