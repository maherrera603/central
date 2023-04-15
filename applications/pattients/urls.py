from django.urls import path
#
from .views import RegisterPattientView


urlpatterns = [
    path('register/', RegisterPattientView.as_view(), name='register_pattient'),
]