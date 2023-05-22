from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

#models
from applications.users.models import Role 
from applications.users.models import User
from .models import Pattient 
from .models import Family

#serializers
from .serializers import RegisterSerilizer
from .serializers import UpdatedSerializer 
from .serializers import FamilySerializer 
from .serializers import UpdateFamilySerializer

# permissions
from applications.users.permissions import IsPattient


# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data["code"] = code
    data["status"] = status
    data["message"] = message
    return data


class RegisterPattientView(APIView):
    def post(self, request):
        serializer = RegisterSerilizer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        user = User.objects.get_user_by_email(serializer.data["email"])
        pattient = Pattient.objects.get_pattient_by_document(serializer.data["document"])
        if user or pattient:
            data = _send_data(400, "bad request", "el usuario ya se encuentra registrado")
            return Response(data)

        rol = Role.objects.get_role("paciente")
        if not rol:
            data = _send_data(404, "not found", "rol no encontrado")
            return Response(data)

        print(f"despues del rol {user} {pattient}")
        
        user = User.objects.create_user(serializer.data["email"], serializer.data["password"], rol)
        pattient = Pattient.objects.create_pattient(serializer.data, user)
        pattient.save()

        data = _send_data(202, "created", "El usuario ha sido creado")
        data["pattient"] = {
            "name": pattient.name,
            "lastname": pattient.lastname,
            "type_document": pattient.type_document,
            "document": pattient.document,
            "phone": pattient.phone
        }
        return Response(data)


class UpdatedPattientView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsPattient]

    def get(self, request, document):
        pattient = Pattient.objects.get_pattient_by_document(document)
        print(pattient)
        if not pattient:
            data = _send_data(404,"not found",  "el usuario no existe")
            return Response(data)

        data = _send_data(200, "OK", "datos del usuario")
        data["pattient"] = {
            "name": pattient.name,
            "lastname": pattient.lastname,
            "type_document": pattient.type_document,
            "document": pattient.document,
            "phone": pattient.phone,
            "eps": pattient.eps,
        }
        
        return Response(data)
        
    def put(self, request, document):
        serializer = UpdatedSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        pattient = Pattient.objects.get_pattient_by_document(document)
        if not pattient:
            data = _send_data(404, "Not Found", "el usuario no se encontro")
            return Response(data)
        
        pattient.name = serializer.data["name"]
        pattient.lastname = serializer.data["lastname"]
        pattient.phone = serializer.data["phone"]
        pattient.eps = serializer.data["eps"]
        pattient.save()
        
        data = _send_data(202, "created", "los datos del usuario han sido actualizado")
        data["pattient"] = {
            "id": pattient.id,
            "name": pattient.name,
            "lastname": pattient.lastname,
            "type_document": pattient.type_document,
            "document": pattient.document,
            "phone": pattient.phone,
            "eps": pattient.eps
        }
        return Response(data)


class FamilyView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsPattient]


    def get(self, request):
        pattient = Pattient.objects.get_user(request.user)
        if not pattient:
            data = _send_data(404, "not found", "usuario no encontrado")
            return Response(data)
        
        families = Family.objects.get_families_by_pattient(pattient)
        data = _send_data(200, "OK", "familiares")
        data["familys"] = families.values()
        return Response(data)

    def post(self, request):
        serializer = FamilySerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos")
            data["errors"] = serializer.errors
            return Response(data)
        
        pattient = Pattient.objects.get_user(request.user)
        if not pattient:
            data = _send_data(404, "not found", "no se encontro usuario")
            return Response(data)
        
        family = Family.objects.get_family_by_document(serializer.data["document"])
        if family:
            data = _send_data(400, "bad request", "el familiar ya ha sido registrado")
            return Response(data)
        
        family = Family.objects.create_family(serializer.data, pattient)
        family.save()
        
        data = _send_data(202, "created", "familiar registrado correctamente")
        data["family"] = {
            "name": family.name,
            "lastname": family.lastname,
            "type_document": family.type_document,
            "document": family.document,
            "phone": family.phone,
            "eps": family.eps,
            "pattient": family.id_pattient.name
        }
        return Response(data)


class DetailFamilyView(APIView):
    authentication_classes = (TokenAuthentication ,)
    permission_classes = [IsPattient]
    
    def get(self, request, document):
        family = Family.objects.get_family_by_document(document)
        if not family:
            data = _send_data(404, "not fount", "familiar no encontrado")
            return Response(data)
        
        data = _send_data(200, 'OK', "datos del familiar")
        data['family'] = {
            "id": family.id,
            "name": family.name,
            "lastname": family.lastname,
            "type_document": family.type_document,
            "document": family.document,
            "phone": family.phone,
            "eps": family.eps
        }
        return Response(data)
    
    def put(self, request, document):
        serializer = UpdateFamilySerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            
        family= Family.objects.get_family_by_document(document)
        if not family:
            data = _send_data(404, "not fount", "familiar no encontrado")
            return Response(data)

        family.name = serializer.data["name"]
        family.lastname = serializer.data["lastname"]
        family.phone = serializer.data["phone"]
        family.save()
        
        data = _send_data(202, "created", "datos del familiar actualizados")
        data["family"] = {
            "id": family.id,
            "name": family.name,
            "lastname": family.lastname,
            "type_document": family.type_document,
            "document": family.document,
            "phone": family.phone,
            "eps": family.eps,
            "pattient": family.id_pattient.name
        }
        return Response(data)
    
    
    def delete(self, request, document):
        family = Family.objects.get_family_by_document(document)
        if not family:
            data = _send_data(404, "not fount", "familiar no encontrado")
            return Response(data)
        
        family.delete()
        
        data = _send_data(204, "not content", "el familiar ha sido eliminado")
        return Response(data)
    
    
class SearchFamilyView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsPattient]
    
    def get(self, request, search):
        user = self.request.user
        pattient = Pattient.objects.get_user(user)
        if not pattient:
            data = _send_data(204, "not found", "El usuario no ha iniciado sesion")
            return Response(data)
        
        familys = Family.objects.search_family(search, pattient)
        if not familys:
            data = _send_data(404, "not found", "No se encontraron resultados")
            return Response(data)
        
        data = _send_data(200, "OK", "familiares")
        data["familys"] = familys.values()
        return Response(data)