from django.urls import path
from .views import FlightView,ReservationsView
from rest_framework import routers

router = routers.DefaultRouter()
router.register("flights", FlightView)
router.register("reservations", ReservationsView)


urlpatterns = []
urlpatterns += router.urls