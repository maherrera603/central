from django.urls import path

# views
from .views import RegisterStatusView 
from .views import DetailStatusView
from .views import RegisterSpcialityView
from .views import DetailSpecialityView


urlpatterns = [
    path("status/", RegisterStatusView.as_view(), name="status"),
    path("status/<str:status>/", DetailStatusView.as_view(), name="status-detail"),
    path("specialitys/", RegisterSpcialityView.as_view(), name="specialitys"),
    path("speciality/<str:speciality>/", DetailSpecialityView.as_view(), name="detail-speciality"),
    
]