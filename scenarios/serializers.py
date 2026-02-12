from rest_framework import serializers
from .models import Scenario

class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'name', 'trigger_condition', 'actions', 'is_active', 'created_at']
