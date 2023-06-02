from django.urls import path

# views
from .views import DetailAdminsitratorView
from .views import RegisterStatusView 
from .views import DetailStatusView
from .views import RegisterSpcialityView
from .views import DetailSpecialityView
from .views import RegisterDoctorView
from .views import DetailDoctorView


urlpatterns = [
    path("profile/<str:document>/", DetailAdminsitratorView.as_view(), name="admin-profile"),
    path("status/", RegisterStatusView.as_view(), name="status"),
    path("status/<str:status>/", DetailStatusView.as_view(), name="status-detail"),
    path("specialitys/", RegisterSpcialityView.as_view(), name="specialitys"),
    path("speciality/<str:speciality>/", DetailSpecialityView.as_view(), name="detail-speciality"),
    path("doctors/", RegisterDoctorView.as_view(), name="doctors"),
    path("doctor/<str:document>/", DetailDoctorView.as_view(), name="detail-doctor"),
    
]