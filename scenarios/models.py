from django.db import models
from devices.models import Device

class Scenario(models.Model):
    name = models.CharField(max_length=100, verbose_name="Scenario Name")
    trigger_condition = models.TextField(verbose_name="Trigger Condition")
    actions = models.TextField(verbose_name="Actions")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

    def __str__(self):
        return self.name
