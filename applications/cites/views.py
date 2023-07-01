from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

# models
from applications.pattients.models import Pattient
from applications.pattients.models import Family
from applications.administrations.models import Speciality
from applications.administrations.models import Status
from applications.administrations.models import Doctor
from applications.employees.models import Employee
from .models import Cites # TODO: change of cites to cite

# serializers
from .serializers import RegisterCiteSerializer
from .serializers import UpdateCiteSerializer
from .serializers import ResponseCiteSerializer

# permissions
from applications.users.permissions import IsEmployee
from applications.users.permissions import IsPattient


# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data
 

class RegisterCiteView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsPattient]
    
    def get(self, request):
        pattient = Pattient.objects.get_user(request.user)
        if not pattient:
            data = _send_data(404, "not found", "el usuario no existe")
            return Response(data)
        
        cites = Cites.objects.get_cites_by_pattient(pattient)
        serializer = ResponseCiteSerializer(cites, many=True)
        data = _send_data(200, "OK", "citas solicitadas")
        data["cites"] = serializer.data
        return Response(data)
    
    def post(self, request):
        serializer = RegisterCiteSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        speciality = Speciality.objects.get_speciality(serializer.data["speciality"])
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no se encontro")
            return Response(data)
        
        status = Status.objects.get_status(serializer.data["status"])
        if not status:
            data = _send_data(404, "not found", "el estado no se encontro")
            return Response(data)
        
        pattient = Pattient.objects.get_user(request.user)
        if not pattient:
            data = _send_data(404, "not found", "no se encontro el usuario")
            return Response(data)
        
        cite = Cites.objects.created_cite(serializer.data, speciality, status, pattient)
        cite.save()
        
        data = _send_data(202, "created", "la cita ha sido solicitada")
        data["cite"] = {
            "name": cite.name,
            "lastname": cite.lastname,
            "type_document": cite.type_document,
            "document": cite.document,
            "phone": cite.phone,
            "eps": cite.eps,
            "specialidad": cite.id_speciality.speciality,
            "status": cite.id_status.status,
            "pattient": cite.id_pattient.name
        }
        return Response(data)
            

class DetailCiteView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsEmployee]
    
    def get(self,request, pk):
        cite = Cites.objects.get_cite_by_pk(pk)
        if not cite:
            data = _send_data(404, "not found", "cita no encontrada")
            return Response(data)
        
        data = _send_data(200, "OK", "Detalle de la cita")
        data["cite"] = {
            "name": cite.name,
            "lastname": cite.lastname,
            "type_document": cite.type_document,
            "document": cite.document,
            "phone": cite.phone,
            "eps": cite.eps,
            "speciality": cite.id_speciality.speciality,
            "doctor": cite.id_doctor.name,
            "date": cite.date_cite,
            "hour": cite.hour_cite,
            "status" : cite.id_status.status
        }
        return Response(data)
    #TODO: remove this method
    def put(self, request, pk):
        serializer = UpdateCiteSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        doctor = Doctor.objects.get_doctor_by_pk(serializer.data["id_doctor"])    
        if not doctor:
            data = _send_data(404, "bad request", "doctor no encontrado")
            return Response(data)
        
        statu = Status.objects.get_status(serializer.data["status"])
        if not statu:
            data = _send_data(404, "not found", "no se encotro el estado")
            return Response(data)
        
        cite = Cites.objects.update_cite(pk, serializer.data, doctor, statu)
        if not cite:
            data = _send_data(404, "not found", "la cita no fue encontrada")
            return Response(data)
        cite.save()
        
        data = _send_data(202, "created", "la cita ha sido actualizada")
        data["cite"] = {
            "name": cite.name,
            "lastname": cite.lastname,
            "type_document": cite.type_document,
            "document": cite.document,
            "phone": cite.phone,
            "eps": cite.eps,
            "speciality": cite.id_speciality.speciality,
            "doctor": cite.id_doctor.name,
            "date_cite": cite.date_cite,
            "hour": cite.hour_cite,
            "status": cite.id_status.status,
        }
        return Response(data)
    
    
class SearchCiteView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsPattient]
    
    def get(self, request, search):
        pattient = Pattient.objects.get_user(request.user)
        cites = Cites.objects.search_cite(pattient, search)
        
        if not pattient:
            data = _send_data(400, "bad request", "El usuario no se ha autenticado")
            return Response(data=data)
        
        if not cites:
            data = _send_data(404, "not found", "No se encontraron resultados")
            return Response(data=data)
        
        serializer = ResponseCiteSerializer(cites, many=True)
        
        data = _send_data(200, "OK", "cita")
        data["cites"] = serializer.data
        return Response(data=data) 
        
                
class AllCitesView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsEmployee]
    
    def get(self, request):
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "el usuario no existe")
            return Response(data)
        
        cites = Cites.objects.all_cites()
        serializer = ResponseCiteSerializer(cites, many=True)
        data = _send_data(200, "OK", "citas solicitadas")
        data["cites"] = serializer.data
        return Response(data)


class SearchCiteForEmployee(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsEmployee]
    
    def get(self, request, search):
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "usuario no encontrado")
            return Response(data)
        
        cites = Cites.objects.get_cite_search(search)
        if cites.count() < 1:
            data = _send_data(404, "not found", "no se encontraron resultados") 
            return Response(data)
        
        serializer = ResponseCiteSerializer(cites, many=True)
        data = _send_data(200, "OK", "lists of cites")
        data["cites"] = serializer.data
        return Response(data)
        
        
class DetailCiteForEmployeeView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsEmployee]
    
    def get(self, request, pk):
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "el usuario no existe")
            return Response(data)
        
        cite = Cites.objects.get_cite_by_pk(pk)
        if not cite:
            data = _send_data(404, "not found", "cita no encontrada")
            return Response(data)
        
        data = _send_data(200, "OK", "data of cite");
        data["cite"] = {
            "name": cite.name,
            "lastname": cite.lastname,
            "type_document": cite.type_document,
            "document": cite.document,
            "phone": cite.phone,
            "eps": cite.eps,
            "speciality": cite.id_speciality.speciality,
            "status": cite.id_status.status,
        }
        return Response(data)