from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100, verbose_name="Gerätename")
    device_type = models.CharField(max_length=50, verbose_name="Gerätetyp")
    status = models.BooleanField(default=False, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellungsdatum")

    def __str__(self):
        return self.name

