from django.db import models
from users.models import User
from equipment.models import Equipment


class RentalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    purpose = models.TextField()
    expire_at = models.DateTimeField()
    approved = models.BooleanField(default=False)


class ProviderRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.TextField()
    approved = models.BooleanField(default=False)
