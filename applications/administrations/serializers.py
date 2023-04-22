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