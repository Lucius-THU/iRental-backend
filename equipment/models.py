from django.db import models
from users.models import User
from common import modeltodict


class Equipment(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=True, default=None,
        on_delete=models.SET_NULL,
        related_name='rented_equipment_set'
    )
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    expire_at = models.DateTimeField()
    rent_until = models.DateTimeField(null=True, default=None)
    launched = models.BooleanField(default=False)
    requesting = models.BooleanField(default=False)
    returning = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def todict(self):
        d = modeltodict(self)
        d['provider'] = self.provider.todict()
        return d
