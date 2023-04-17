from rest_framework import serializers

class RegisterSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    type_document = serializers.CharField(max_length=50)
    document = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=70)
    password = serializers.CharField()
    
    def validate(self, data):
        password = data['password']
        if len(password) < 8 or len(password) > 12:
            raise serializers.ValidationError("La Contraseña debe tener de 8 a 12 caracteres")
        return data    