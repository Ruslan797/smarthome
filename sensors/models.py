from django.db import models
from devices.models import Device  # Import the Device model from the devices app

class Sensor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Sensor Name")
    sensor_type = models.CharField(max_length=50, verbose_name="Sensor Type")
    value = models.FloatField(verbose_name="Current Value")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="Device")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

    def __str__(self):
        return self.name
