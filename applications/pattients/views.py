from django.shortcuts import render
#
from rest_framework.views import APIView
from rest_framework.response import Response
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
        rol = Role.objects.get_rol(3)
        user = User.objects.create_user(serializer.data['email'], serializer.data['password'], rol)
        pattient = Pattient.objects.create_pattient(serializer.data, user)
        data = _send_data(201, 'created', 'El registro fue exitoso')
        data['pattient'] = serializer.data
        return Response(data)