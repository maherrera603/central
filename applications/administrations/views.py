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
from applications.users.permissions import IsEmployee

#serializers

from .serializers import StatusSerializer 
from .serializers import SpecialityResponseSerializer
from .serializers import SpecialitySerializer
from .serializers import DoctorResponseSerializer
from .serializers import DoctorSerializer
from .serializers import AdministratorSerializer
from applications.employees.serializers import EmployeeResponseSerializer



# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data


class DetailAdminsitratorView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request, document):
        admin = Employee.objects.get_employee_by_document(document)
        if not admin: 
            data = _send_data(404, "not found", "administrador no encontrado")
            return Response(data)
        
        serializer = EmployeeResponseSerializer(admin)
        data = _send_data(202, "OK", "datos del administrador")
        data["employee"] = serializer.data
        return Response(data)
    
    def put(self, request, document):
        admin = Employee.objects.get_user(request.user)
        if not admin:
            data = _send_data(404, "not found", "El usuario no existe")
            return Response(data)
        
        serializer = AdministratorSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "Complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)
        
        adminUpdate = Employee.objects.updated_employee(document, serializer.data)
        if not adminUpdate:
            data = _send_data(400, "bad request", "Error a actualizar datos del usuario")
            return Response(data)
        adminUpdate.save()
        
        serializer_admin = EmployeeResponseSerializer(adminUpdate)
        data = _send_data(201, "created", "datos actualizados correctamente")
        data["admin"] = serializer_admin.data
        return Response(data)
        
        
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
        serializer = SpecialityResponseSerializer(specialitys, many=True)
        data["specialitys"] = serializer.data
        return Response(data)
    
    def post(self, request):
        serializer = SpecialityResponseSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos del formulario")
            data["errors"] = serializer.errors
            return Response(data)
            
        speciality = Speciality.objects.get_speciality(serializer.data["speciality"])
        if speciality:
            data = _send_data(400, "bad request", "la especialidad ya ha sido registrada")
            return Response(data)
        
        
        employee = Employee.objects.get_user(request.user)
        speciality = Speciality.objects.create_speciality(serializer.data, employee)
        speciality.save()
        data = _send_data(202, "created", "la especialidad ha sido registrada")
        data["speciality"] = serializer.data
        return Response(data)


class SearchSpecialityView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]

    def get(self, request, speciality):
        admin = Employee.objects.get_user(request.user)
        if not admin:
            data = _send_data(404, "not found", "No se encontro el administrador")
            return Response(data)
        
        specialitys = Speciality.objects.search_speciality(speciality)
        if not specialitys:
            data = _send_data(404, "not found", "No se encontraron resultados")
            return Response(data)
        
        serializer = SpecialityResponseSerializer(specialitys, many=True)
        data = _send_data(200, "OK", "listado de especialidades")
        data["specialitys"] = serializer.data
        return Response(data)


class DetailSpecialityView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request, pk):
        speciality = Speciality.objects.get_speciality_by_pk(pk)
        if not speciality:
            data = _send_data(404, "not found", "Especialidad no econtrada")
            return Response(data)
        
        serializer = SpecialityResponseSerializer(speciality)
        data = _send_data(200, "OK", "Detalle especialidad")
        data["speciality"] = serializer.data
        return Response(data)
    
    def put(self, request, pk):
        serializer = SpecialityResponseSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos del formulario")
            data["errors"] = serializer.errors
            return Response(data)
        
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "El empleado no se encontro")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality_by_pk(pk)
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no se encontro")
            return Response(data)

        speciality.speciality = serializer.data["speciality"]
        speciality.employee = employee
        speciality.save()
        
        data = _send_data(202, "created", "especialidad Actualizada")
        data["specialiity"] = serializer.data
        return Response(data)
        
    def delete(self, request, pk):
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "el empleado no se encontro")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality_by_pk(pk)
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
        serializer = DoctorResponseSerializer(doctors, many=True)
        data["doctors"] = serializer.data
        return Response(data)
    
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos correctamente")
            data["errors"] = serializer.errors
            return Response(data)
        
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "el empleado no se encontro")
            return Response(data)
        
        doctor = Doctor.objects.get_doctor_by_document(serializer.data["document"])
        if doctor:
            data = _send_data(400, "bad request", "el doctor ya ha sido registrado correctamente")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality_by_pk(serializer.data["speciality"])
        if not speciality:
            data = _send_data(404, "not found", "la especialidad no fue encontrada")
            return Response(data)
        
        status = Status.objects.get_status(serializer.data["status"])
        if not status:
            data = _send_data(404, "not found", "el status no fue encontrado")
            return Response(data)
        
        doctor = Doctor.objects.created_doctor(serializer.data, employee, speciality, status)
        doctor.save()
        serializer_doctor = DoctorResponseSerializer(doctor)
        data = _send_data(202, "created", "el doctor ha sido añadido")
        data["doctor"] = serializer_doctor.data
        return Response(data)
    
    
class DetailDoctorView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request, document):
        doctor = Doctor.objects.get_doctor_by_document(document)
        if not doctor:
            data = _send_data(404, "not found", "el doctor no se encontro")
            return Response(data)
        
        serializer = DoctorSerializer(doctor)
        data = _send_data(200, "OK", "datos del doctor")
        data["doctor"] = serializer.data
        return Response(data)
    
    def put(self, request, document):
        serializer = DoctorSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "complete los campos")
            data["errors"] = serializer.errors 
            return Response(data)
        
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "no se encontro el empleado")
            return Response(data)
        
        speciality = Speciality.objects.get_speciality_by_pk(serializer.data["speciality"])
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
        serializer_doctor = DoctorResponseSerializer(doctor)
        
        data = _send_data(202, "created", "los datos del doctor han sido actualizados")
        data["doctor"] = serializer_doctor.data 
        return Response(data)
    
    def delete(self, request, document):
        doctor = Doctor.objects.get_doctor_by_document(document)
        if not doctor:
            data = _send_data(404, "not found", "no se encontro el doctor")
            return Response(data)
        
        doctor.delete()

        data = _send_data(204, "not content", "el doctor ha sido eliminado")
        return Response(data)


class SearchDoctorView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]

    def get(self, request, search):
        admin = Employee.objects.get_user(request.user)
        if not admin:
            data = _send_data(404, "not found", "El Usuario no se encontro")
            return Response(data)
        
        doctors = Doctor.objects.search_doctor(search)
        if not doctors:
            data = _send_data(404, "not found", "No se encontraron resultados")
            return Response(data)
        serializer = DoctorResponseSerializer(doctors, many=True)
        data = _send_data(200, "OK", "listado de doctores")
        data["doctors"] = serializer.data
        return Response(data)
    
    
class DoctorBySpciality(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsEmployee]
    
    def get(self, request, pk):
        employee = Employee.objects.get_user(request.user)
        if not employee:
            data = _send_data(404, "not found", "El Usuario no se encontro")
            return Response(data)
        
        doctors = Doctor.objects.get_doctor_by_speciality(pk)
        if len(doctors) == 0:
            data = _send_data(404, "not found", "No se encontraron resultados")
            return Response(data)
        
        serializer = DoctorResponseSerializer(doctors, many=True)
        data = _send_data(200, "OK", "listado de doctores")
        data["doctors"] = serializer.data
        return Response(data)