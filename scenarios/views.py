from rest_framework import generics
from .models import Scenario
from .serializers import ScenarioSerializer

class ScenarioListCreateView(generics.ListCreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

class ScenarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
