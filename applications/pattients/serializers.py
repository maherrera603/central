from rest_framework import serializers

#models
from .models import Pattient
from .models import Family

# serializers
from applications.users.serializers import UserResponseSerializer
from applications.users.serializers import LoginSerializer


class PattientResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(write_only=False)
    document = serializers.CharField(write_only=False)
    class Meta:
            model = Pattient
            fields = ["id", "name", "last_name", "type_document", "document", "phone", "eps","user"]


class RegisterSerilizer(serializers.ModelSerializer):
    user = LoginSerializer()
    document = serializers.CharField(write_only=False)
    
    class Meta:
        model = Pattient
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "user"]
    
    def validate_name(self, data):
        if len(data) <= 3 or len(data) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return data
    
    
class UpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattient
        fields = ["name", "last_name", "phone", "eps"]
    

    
class FamilySerializer(serializers.ModelSerializer):
    pattient = PattientResponseSerializer(read_only=True)
    
    class Meta:
        model = Family
        exclude =  ["created_at", "updated_at"]
    
        
class UpdateFamilySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)
    eps = serializers.CharField(max_length=50)