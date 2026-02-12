from django.urls import path
from .views import SensorListCreateView, SensorRetrieveUpdateDestroyView

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('sensors/<int:pk>/', SensorRetrieveUpdateDestroyView.as_view(), name='sensor-retrieve-update-destroy'),
]
