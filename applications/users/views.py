from django.shortcuts import render
from django.contrib import auth
#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# models
from applications.pattients.models import Pattient
from applications.employees.models import Employee
# serializers
from .serializers import LoginSerializer

# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        account = auth.authenticate(email=email, password=password)
        if account is None:
            data = _send_data(400, 'bad request', 'El correo y/o contraseña son incorrectos, intentelo de nuevo')
            return Response(data)
        
        Table = Pattient if account.id_role.id == 3 else Employee
        user = Table.objects.get_user(account)
        token = Token.objects.get_or_create(user=account)[0]
        
        data = _send_data(200, 'OK', 'Login Correcto')
        data['token'] = token.key
        data['pattient'] = {
            'name': user.name,
            'lastname': user.lastname,
            'type_document': user.type_document,
            'document': user.document,
            'phone': user.phone,
            'email': account.email,
            'role': account.id_role.id
        }
        return Response(data)
    
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        request.user.auth_token.delete()
        data = _send_data(204, 'not content', 'sesion cerrada exitosamente')
        return Response(data)