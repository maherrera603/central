from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    
    def validate_status(self, status):
        if len(status) < 3 or len(status) > 20:
            raise serializers.ValidationError("El estado debe contener de 3 a 20 caracteres")
        return status


class SpecialitySerializer(serializers.Serializer):
    speciality = serializers.CharField()
    
    def validate_speciality(self, speciality):
        if len(speciality) < 3 or len(speciality) > 40:
            raise serializers.ValidationError("la specialidad debe contener mas de 3 caracteres")
        return speciality
    
    
class DoctorSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField()
    type_document = serializers.CharField()
    document = serializers.CharField()
    phone = serializers.CharField()
    speciality = serializers.CharField()
    status = serializers.CharField()
    
    
    def validate_name(self, data):
        if len(data) < 3 or len(data) > 20:
            raise serializers.ValidationError("El campo debe contener de 3 a 20 caracteres")
        return data
    
    def validate_lastname(self, data):
        if len(data) < 3 or len(data) >20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return data
    
    def validate_type_document(self, data):
        if len(data) < 3 or len(data) > 30:
            raise serializers.ValidationError("el campo debe contener de 3 a 30 caracteres")
        return data
    
    def validate_document(self, data):
        if len(data) < 6 or len(data) > 20:
            raise serializers.ValidationError("el campo debe contener de 6 a 20 caracteres")
        return data 
    
    def validate_phone(self, data):
        if len(data) < 10 or len(data) >10:
            raise serializers.ValidationError("el campo debe contener 10 caracteres")
        return data
    
    def validate_speciality(self, data):
        if len(data) < 5 or len(data) > 30:
            raise serializers.ValidationError("el campo debe contener de 5 a 30 caracteres")
        return data
    
    def validate_status(self, data):
        if len(data) < 5 or len(data) > 30:
            raise serializers.ValidationError("el campo debe contener de 5 a 30 caracteres")
        return data