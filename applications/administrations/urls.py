from django.urls import path

# views
from .views import DetailAdminsitratorView
from .views import RegisterStatusView 
from .views import DetailStatusView
from .views import RegisterSpcialityView
from .views import DetailSpecialityView
from .views import SearchSpecialityView
from .views import RegisterDoctorView
from .views import DetailDoctorView
from .views import SearchDoctorView
from .views import DoctorBySpciality


urlpatterns = [
    path("profile/<str:document>/", DetailAdminsitratorView.as_view(), name="admin-profile"),
    path("status/", RegisterStatusView.as_view(), name="status"),
    path("status/<str:status>/", DetailStatusView.as_view(), name="status-detail"),
    path("specialitys/", RegisterSpcialityView.as_view(), name="specialitys"),
    path("speciality/<int:pk>/", DetailSpecialityView.as_view(), name="detail-speciality"),
    path("specialitys/search/<str:speciality>/", SearchSpecialityView.as_view(), name="search-speciality"),
    path("doctors/", RegisterDoctorView.as_view(), name="doctors"),
    path("doctor/<str:document>/", DetailDoctorView.as_view(), name="detail-doctor"),
    path("doctors/search/<str:search>/", SearchDoctorView.as_view(), name="search-doctor"),
    path("doctor/speciality/<int:pk>/", DoctorBySpciality.as_view(), name="doctor-speciality"), 
]