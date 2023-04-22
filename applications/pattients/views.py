from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
        serializer.is_valid(raise_exception=True)
        if User.objects.user_exists(serializer.data["email"]):
            data = _send_data(404, "bad request", "El usuario ya se encuentra registrado")
            return Response(data)

        rol = Role.objects.get_rol(3)
        user = User.objects.create_user(serializer.data["email"], serializer.data["password"], rol)
        pattient = Pattient.objects.create_pattient(serializer.data, user)
        data = _send_data(201, "created", "El registro fue exitoso")
        data["pattient"] = serializer.data
        return Response(data)


class UpdatedPattientView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get(self, request, document):
        pattient = Pattient.objects.get_pattient(document)
        data = _send_data(200, "OK", "datos del paciente")
        data["pattient"] = {
            "name": pattient.name,
            "lastname": pattient.lastname,
            "type_document": pattient.type_document,
            "document": pattient.document,
            "phone": pattient.phone
        }
        return Response(data)

    def patch(self, request, document):
        serializer = UpdatedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pattient = Pattient.objects.update_pattient(document, serializer.data)
        pattient.save()
        data = _send_data(202, "created", "actualizacion de datos existosa")
        data["pattient"] = {
            "id": pattient.id,
            "name": pattient.name,
            "lastname": pattient.lastname,
            "type_document": pattient.type_document,
            "document": pattient.document,
            "phone": pattient.phone,
            "email": pattient.id_user.email
        }
        return Response(data)


class FamilyView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    serializer_class = FamilySerializer

    def get(self, request):
        pattient = Pattient.objects.get_pattient_by_id_user(request.user.id)
        familys = Family.objects.obtain_familys(pattient.id)
        print(familys.values_list())
        data = _send_data(200, "OK", "Listado de familiares")
        data['familys'] = familys.values()
        return Response(data)

    def post(self, request):
        serializer = FamilySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pattient = Pattient.objects.get_pattient_by_id(serializer.data['id_pattient'])
        family = Family.objects.create_family(serializer.data, pattient)
        family.save()
        data = _send_data(202, "created", "familiar registrado correctamente")
        data["family"] = {
            "name": family.name,
            "lastname": family.lastname,
            "type_document": family.type_document,
            "document": family.document,
            "phone": family.phone,
            "pattient": family.id_pattient.name
        }
        return Response(data)


class DetailFamilyView(APIView):
    authentication_classes = (TokenAuthentication ,)
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        family = Family.objects.get_family_by_id(pk)
        if family["exists"] is False:
            data = _send_data(404, "not fount", "familiar no encontrado")
            return Response(data)
        data = _send_data(200, 'OK', "datos del familiar")
        data['family'] = {
            "id": family["family"].id,
            "name": family["family"].name,
            "lastname": family["family"].lastname,
            "type_document": family["family"].type_document,
            "document": family["family"].document,
            "phone": family["family"].phone
        }
        return Response(data)
    
    def put(self, request, pk):
        serializer = UpdateFamilySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        family= Family.objects.get_family_by_id(pk)
        if family["exists"] is False:
            data = _send_data(404, "not fount", "familiar no encontrado")
            return Response(data)

        familyData = family["family"]
        familyData.name = serializer.data["name"]
        familyData.lastname = serializer.data["lastname"]
        familyData.phone = serializer.data["phone"]
        familyData.save()
        data = _send_data(202, "created", "datos del familiar actualizados")
        data["family"] = {
            "id": familyData.id,
            "name": familyData.name,
            "lastname": familyData.lastname,
            "type_document": familyData.type_document,
            "document": familyData.document,
            "phone": familyData.phone,
            "pattient": familyData.id_pattient.name
        }
        return Response(data)
    
    
    def delete(self, request, pk):
        family = Family.objects.get_family_by_id(pk)
        if family["exists"] is False:
            data = _send_data(404, "not fount", "familiar no encontrado")
            return Response(data)
        family_deleted = family["family"]
        family_deleted.delete()
        data = _send_data(204, "not content", "el familiar ha sido eliminado")
        return Response(data)