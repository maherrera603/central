from django.shortcuts import render
#
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data['code'] = code
    data['status'] = status
    data['message'] = message
    return data

class RegisterPattientView(APIView):
    def post(self, request):
        data = _send_data(200, 'OK', 'pattient has been registered')
        return Response(data)