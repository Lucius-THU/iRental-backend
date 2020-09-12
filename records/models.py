from django.db import models
from users.models import User
from equipment.models import Equipment
from common import modeltodict


class RentalRecord(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.SET_NULL)
    returned = models.BooleanField(default=False)

    def todict(self):
        d = modeltodict(self)
        d['user'] = self.user.todict()
        d['equipment'] = self.equipment.todict()
        return d
