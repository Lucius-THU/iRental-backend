from django.db import models
from users.models import User
from equipment.models import Equipment
from common import modeltodict


class RentalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    purpose = models.TextField()
    rent_until = models.DateTimeField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def todict(self):
        d = modeltodict(self)
        d['user'] = self.user.todict()
        d['equipment'] = self.equipment.todict()
        return d


class ProviderRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.TextField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def todict(self):
        d = modeltodict(self)
        d['user'] = self.user.todict()
        return d
