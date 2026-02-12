from django.contrib import admin
from .models import Sensor

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sensor_type', 'value', 'device', 'created_at')
    list_filter = ('sensor_type', 'device')
    search_fields = ('name', 'sensor_type')
