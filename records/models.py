from django.db import models
from users.models import User


class RentalRecord(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    returned = models.BooleanField(default=False)
