from django.contrib import auth

# rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# models
from applications.pattients.models import Pattient
from applications.employees.models import Employee
from .models import Role 
from .models import User

# serializers
from .serializers import SuperUserSerializer 
from .serializers import RoleSerializer
from .serializers import LoginSerializer

# permissions
from .permissions import IsAdministrator
from .permissions import IsEmployee
from .permissions import IsPattient


# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data


class CreateSuperUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SuperUserSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "Complete los campos requeridos")
            data["error"] = serializer.errors
            return Response(data)
        
        user_exists = User.objects.user_exists(serializer.data["email"])
        if user_exists is not False: 
            data = _send_data(400, "bad request", "El usuario ya se encuentra registrado")
            return Response(data)

        user = User.objects.create_superuser(email=serializer.data["email"], password=serializer.data["password"])
        data = _send_data(202, "created", "the superuser has been created")
        return Response(data)


class RegisterRoleView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator] # TODO: add or change permissions of admin
    
    def get(self, request):
        roles = Role.objects.get_all_roles()
        data = _send_data(200, "OK", "roles")
        data["roles"] = roles.values()
        return Response(data)
    
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "Ha ocurrido un error, intentelo de nuevo")
            data["errors"] = serializer.errors["role"] = "el role ya se encuentra registrado"
            return Response(data)
        
        serializer.save()
        data = _send_data(202, 'created', 'rol registrado correctamente')
        data['role'] = serializer.data
        return Response(data)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            return Response(data)
        
        email = serializer.data['email']
        password = serializer.data['password']
        account = auth.authenticate(email=email, password=password)
        if account is None:
            data = _send_data(400, 'bad request', 'El correo y/o contraseña son incorrectos, intentelo de nuevo')
            return Response(data)
        
        Table = Pattient if account.id_role.id == 3 else Employee
        user = Table.objects.get_user(account)
        if not user:
            data = _send_data(404, "not found", "el usuario no existe")
            return Response(data)
        
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
    permission_classes = [IsAdministrator|IsEmployee|IsPattient]

    def delete(self, request):
        request.user.auth_token.delete()
        data = _send_data(204, 'not content', 'sesion cerrada exitosamente')
        return Response(data)
