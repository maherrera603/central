from django.shortcuts import render
#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

# models
from applications.employees.models import Employee
from .models import Status
from .models import Speciality
from .models import Doctor

# permissions
from applications.users.permissions import IsAdministrator

#serializers
from .serializers import StatusSerializer 
from .serializers import SpecialitySerializer
from .serializers import DoctorSerializer


# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data


# TODO: implement views for doctors
class RegisterStatusView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request):
        status = Status.objects.get_all_status()
        data = _send_data(200, "OK", "listado de status")
        data["list_status"] = status.values()
        return Response(data)
    
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos del formulario")
            data["errors"] = serializer.errors
            return Response(data)

        status = Status.objects.get_status(serializer.data["status"])
        if status:
            data = _send_data(400, "bad request", "El estado ya ha sido registrado anteriormente")
            return Response(data)
        
        status = Status.objects.create_status(serializer.data)
        status.save()
        data = _send_data(202, "created", "Estado registrado")
        data["estado"] = serializer.data
        return Response(data)
    
    
class DetailStatusView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request, status):
        status = Status.objects.get_status(status=status)
        if not status:
            data = _send_data(404, "not content", "no se encontro el estado")
            return Response(data)
                
        data = _send_data(200, "OK", "detalle del status")
        data["detail"] = {
            "id": status.id,
            "status": status.status
        }
        return Response(data)
    
    def put(self, request, status):
        serializer = StatusSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos del formulario")
            data["errors"] = serializer.errors
            return Response(data)
        
        status = Status.objects.get_status(status)
        if not status:
            data = _send_data(404, "not found", "El estado no se encuentra registrado")
            return Response(data)

        updated_status = Status.objects.updated_status(status, serializer.data)
        updated_status.save()
        
        data = _send_data(202, "created", "El estado ha sido actualizado correctamente")
        data["status_update"] = {
            "id": updated_status.id,
            "status": updated_status.status
        }
        return Response(data)
    
    def delete(self, request, status):
        status = Status.objects.get_status(status)
        if not status:
            data = _send_data(404, "not found", "El estado no se encontro")
        
        status.delete()
        data = _send_data(204, "not content", "El estado ha sido eliminado correctamente")
        return Response(data)


class RegisterSpcialityView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request):
        specialitys = Speciality.objects.get_all_specialities()
        data = _send_data(200, "OK", "listado de especialidades")
        data["specialitys"] = specialitys.values()
        return Response(data)
    
    def post(self, request):
        serializer = SpecialitySerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos del formulario")
            data["errors"] = serializer.errors
            return Response(data)
            
        speciality = Speciality.objects.get_speciality(serializer.data["speciality"])
        if speciality:
            data = _send_data(400, "bad request", "la especialidad ya ha sido registrada")
            return Response(data)
        
        
        employee = Employee.objects.get_employee_by_user(request.user)
        speciality = Speciality.objects.create_speciality(serializer.data, employee)
        speciality.save()
        data = _send_data(202, "created", "la especialidad ha sido registrada")
        data["speciality"] = {
            "id" : speciality.id,
            "speciality": speciality.speciality,
            "id_employee": speciality.id_employee.id
        }
        return Response(data)


class DetailSpecialityView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request, speciality):
        speciality = Speciality.objects.get_speciality(speciality)
        if not speciality:
            data = _send_data(404, "not found", "Especialidad no econtrada")
            return Response(data)
        
        data = _send_data(200, "OK", "Detalle especialidad")
        data["speciality"] = {
            "id": speciality.id,
            "speciality": speciality.speciality
        }
        return Response(data)
    
    def put(self, request, speciality):
        serializer = SpecialitySerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos del formulario")
            data["errors"] = serializer.errors
            return Response(data)
        
        employee = Employee.objects.get_employee_by_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "El empleado no se encontro")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality(speciality)
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no se encontro")
            return Response(data)

        speciality.speciality = serializer.data["speciality"]
        speciality.id_employee = employee
        speciality.save()
        
        data = _send_data(202, "created", "especialidad creada")
        data["specialiity"] = {
            "id": speciality.id,
            "speciality": speciality.speciality,
            "employee": speciality.id_employee.id
        }
        return Response(data)
        
    def delete(self, request, speciality):
        employee = Employee.objects.get_employee_by_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "el empleado no se encontro")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality(speciality)
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no se encontro")
            return Response(data)
        
        speciality.delete()
        
        data = _send_data(204, "not content", "la especialidad ha sido eliminada")
        return Response(data)


class RegisterDoctorView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request):
        doctors = Doctor.objects.get_all_doctors()
        data = _send_data(200, "OK", "listado de doctores")
        data["doctors"] = doctors.values()
        return Response(data)
    
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos correctamente")
            data["errors"] = serializer.errors
            return Response(data)
        
        employee = Employee.objects.get_employee_by_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "el empleado no se encontro")
            return Response(data)
        
        doctor = Doctor.objects.get_doctor_by_document(serializer.data["document"])
        if doctor:
            data = _send_data(400, "bad request", "el doctor ya ha sido registrado correctamente")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality(serializer.data["speciality"])
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no fue encontrada")
            return Response(data)
        
        status = Status.objects.get_status(serializer.data["status"])
        if not status:
            data = _send_data(404, "not found", "el status no fue encontrado")
            return Response(data)
        
        doctor = Doctor.objects.created_doctor(serializer.data, employee, speciality, status)
        doctor.save()
        
        data = _send_data(202, "created", "el doctor ha sido añadido")
        data["doctor"] = {
            "id": doctor.id,
            "name": doctor.name,
            "lastname": doctor.lastname,
            "type_document": doctor.type_document,
            "document": doctor.document,
            "id_speciality": doctor.id_speciality.id,
            "id_status": doctor.id_status.id,
            "id_employee": doctor.id_employee.id
        } 
        return Response(data)
    
    
class DetailDoctorView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request, document):
        doctor = Doctor.objects.get_doctor_by_document(document)
        if not doctor:
            data = _send_data(404, "not found", "el doctor no se encontro")
            return Response(data)
        
        data = _send_data(200, "OK", "datos del doctor")
        data["doctor"] = {
            "id": doctor.id,
            "name": doctor.name,
            "lastname": doctor.lastname,
            "type_document": doctor.type_document,
            "document": doctor.document,
            "phone": doctor.phone,
            "speciality": doctor.id_speciality.speciality,
            "status": doctor.id_status.status
        }
        return Response(data)
    
    def put(self, request, document):
        serializer = DoctorSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos")
            data["errors"] = serializer.errors 
            return Response(data)
        
        employee = Employee.objects.get_employee_by_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "no se encontro el empleado")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality(serializer.data["speciality"])
        if not speciality:
            data = _send_data(404, "not found", "no se encontro la especialidad")
            return Response(data)
        
        status = Status.objects.get_status(serializer.data["status"])
        if not status:
            data = _send_data(404, "not found", "el estado no se encontro")
            return Response(data)
       
        doctor = Doctor.objects.updated_doctor(document, serializer.data, speciality, status, employee)
        if not doctor:
            data = _send_data(404, "not found", "no se econtro el doctor")
            return Response(data)
        doctor.save()
                 
        data = _send_data(202, "created", "los datos del doctor han sido actualizados")
        data["doctor"] = {
            "id": doctor.id,
            "name": doctor.name,
            "lastname": doctor.lastname,
            "type_document": doctor.type_document,
            "document": doctor.document,
            "phone": doctor.phone,
            "speciality": doctor.id_speciality.speciality,
            "status": doctor.id_status.status
        } 
        return Response(data)
    
    def delete(self, request, document):
        doctor = Doctor.objects.get_doctor_by_document(document)
        if not doctor:
            data = _send_data(404, "not found", "no se encontro el doctor")
            return Response(data)
        
        doctor.delete()

        data = _send_data(204, "not content", "el doctor ha sido eliminado")
        return Response(data)
        
        