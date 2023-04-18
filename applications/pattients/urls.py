from django.urls import path
#
from .views import RegisterPattientView, UpdatedPattientView


urlpatterns = [
    path('register/', RegisterPattientView.as_view(), name='register_pattient'),
    path('pattient/<str:document>/', UpdatedPattientView.as_view(), name='updated_pattient'),
]