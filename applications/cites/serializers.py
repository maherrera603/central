from datetime import datetime
#
from rest_framework import serializers

# models 
from .models import Cites
from applications.administrations.models import Status

# serializers
from applications.administrations.serializers import StatusSerializer
from applications.pattients.serializers import PattientResponseSerializer
from applications.administrations.serializers import StatusResponseSerializer
from applications.administrations.serializers import SpecialityResponseSerializer
from applications.administrations.serializers import DoctorResponseSerializer


class CiteResponseSerializer(serializers.ModelSerializer):
    pattient = PattientResponseSerializer(write_only=False)
    status = StatusResponseSerializer(write_only=False)
    speciality = SpecialityResponseSerializer(write_only=False)
    
    class Meta: 
        model = Cites
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "eps", "speciality", "doctor", "status",  "date_cite", "hour_cite", "pattient"]


class RegisterCiteSerializer(serializers.ModelSerializer):
    status = StatusResponseSerializer(write_only=False)
    pattient = PattientResponseSerializer(write_only=False)
    
    class Meta:
        model = Cites
        fields = ["name", "last_name", "type_document", "document", "phone", "eps", "speciality", "status", "pattient"]
    
    
class UpdateCiteSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField()
    type_document = serializers.CharField()
    document = serializers.CharField()
    phone = serializers.CharField()
    eps = serializers.CharField()
    speciality = serializers.CharField()
    id_doctor = serializers.IntegerField()
    date_cite = serializers.DateField()
    hour_cite = serializers.TimeField(format='%I:%M:%S')
    status = serializers.CharField()
    
    # def validate_date_cite(self, date_cite):
    #     date_cite = datetime.strptime(str(date_cite), "%d-%m-%Y")
    #     return date_cite
    
    # def validate_hour_cite(self, hour_cite):
    #     return datetime.strptime(str(hour_cite, "%I:%S:%M %p"))
        
    
    def validate_status(self, status):
        if len(status) < 3 or len(status) > 20:
            raise serializers.ValidationError("el campo debe contener de 3 a 20 caracteres")
        return status
    

class ResponseCiteSerializer(serializers.ModelSerializer):
    id_status = serializers.SlugRelatedField( read_only=True, slug_field="status" )
    id_speciality = serializers.SlugRelatedField( read_only=True, slug_field="speciality" )
    id_doctor = serializers.SlugRelatedField( read_only=True, slug_field="name" )
    
    class Meta:
        model = Cites
        fields = "__all__"


class CiteSerializer(serializers.ModelSerializer):
    pattient = PattientResponseSerializer(write_only=False)
    status = StatusResponseSerializer(write_only=False)
    speciality = SpecialityResponseSerializer(write_only=False)
    doctor = DoctorResponseSerializer(write_only=False)
    
    class Meta: 
        model = Cites
        fields = ["id", "name", "last_name", "type_document", "document", "phone", "eps", "speciality", "doctor", "status",  "date_cite", "hour_cite", "pattient"]
