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
from .serializers import CiteResponseSerializer
from .serializers import RegisterCiteSerializer
from .serializers import UpdateCiteSerializer
from .serializers import ResponseCiteSerializer
from .serializers import CiteSerializer

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
        serializer = CiteResponseSerializer(cites, many=True)
        data = _send_data(200, "OK", "citas solicitadas")
        data["cites"] = serializer.data
        return Response(data)
    
    def post(self, request):
        serializer = RegisterCiteSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        speciality = Speciality.objects.get_speciality_by_pk(serializer.data["speciality"])
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no se encontro")
            data["serializer"] = serializer.data["speciality"]
            return Response(data)
        
        status = Status.objects.get_status(serializer.data["status"]["id"])
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
        data["cite"] = serializer.data
        return Response(data)
            

class DetailCiteView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsPattient]
    
    def get(self,request, pk):
        cite = Cites.objects.get_cite_by_pk(pk)
        if not cite:
            data = _send_data(404, "not found", "cita no encontrada")
            return Response(data)
        
        serializer = CiteSerializer(cite)
        data = _send_data(200, "OK", "Detalle de la cita")
        data["cite"] = serializer.data
        return Response(data)
    
    def delete(self, request, pk):
        pattient = Pattient.objects.get_user(request.user)
        if not pattient:
            data = _send_data(401, "Unauthorized", "No Ha Iniciado Sesion")
            return Response(data)
        
        cite = Cites.objects.get_cite_by_pk(pk)
        if not cite:
            data = _send_data(404, "not found", "Cita no encontrada")
            return Response(data)
        
        cite.delete();
        data = _send_data(204, "not content", "Cita eliminada correctamente")
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
        serializer = CiteResponseSerializer(cites, many=True)
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
        
        serializer = CiteResponseSerializer(cite)
        data = _send_data(200, "OK", "data of cite");
        data["cite"] = serializer.data
        return Response(data)
    
    def put(self, request, pk):
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(400, "bad request", "el usuario no existe")
            return Response(data)
        
        serializer = CiteResponseSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "Complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        
        status = Status.objects.get_status(serializer.data["status"]["id"])
        if not status: 
            data = _send_data(404, "not found", "El estado no se encontro")
            return Response(data)
        
        doctor = Doctor.objects.get_doctor_by_pk(serializer.data["doctor"])
        if not doctor:
            data = _send_data(404, "not found", "El doctor no se encontro")
            return Response(data)
        
        cite = Cites.objects.update_cite(pk, serializer.data, doctor, status)
        cite.save()
        
        data = _send_data(202, "created", "La cita ha sido actualizada")
        data["cite"] = serializer.data
        return Response(data)