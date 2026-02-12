from django.urls import path
from .views import ScenarioListCreateView, ScenarioRetrieveUpdateDestroyView

urlpatterns = [
    path('scenarios/', ScenarioListCreateView.as_view(), name='scenario-list-create'),
    path('scenarios/<int:pk>/', ScenarioRetrieveUpdateDestroyView.as_view(), name='scenario-retrieve-update-destroy'),
]
