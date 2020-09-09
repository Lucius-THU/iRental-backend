from django.db import models
from users.models import User


class RentalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProviderRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
