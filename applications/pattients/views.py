from django.shortcuts import render
#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
#models
from applications.users.models import Role, User
from .models import Pattient
#serializers
from .serializers import RegisterSerilizer

# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data

class RegisterPattientView(APIView):
    def post(self, request):
        serializer = RegisterSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if User.objects.user_exists(serializer.data['email']):
            data = _send_data(404, 'bad request', 'El usuario ya se encuentra registrado')
            return Response(data)
        
        rol = Role.objects.get_rol(3)
        user = User.objects.create_user(serializer.data['email'], serializer.data['password'], rol)
        pattient = Pattient.objects.create_pattient(serializer.data, user)
        data = _send_data(201, 'created', 'El registro fue exitoso')
        data['pattient'] = serializer.data
        return Response(data)


class UpdatedPattientView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document):
        pattient = Pattient.objects.get_pattient(document)
        data = _send_data(200, 'OK', "datos del paciente")
        data['pattient'] = {
            'name': pattient.name,
            'lastname': pattient.lastname,
            'type_document': pattient.type_document,
            'document': pattient.document,
            'phone': pattient.phone
        }
        return Response(data)
    
    def patch(self, request, document):
        return Response('update pattient')
    
    