from django.urls import path

from api.flight.views import FlightDetail, FlightList
from api.user.views import RegisterView

urlpatterns = [
    path("flight/<int:id>", FlightDetail.as_view(), name="flight_detail"),
    path("flight/", FlightList.as_view(), name="flight_list"),
    path("register/", RegisterView.as_view(), name="auth_register"),
]
