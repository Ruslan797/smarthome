from rest_framework import serializers
from .models import Sensor

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensor_type', 'value', 'device', 'created_at']

