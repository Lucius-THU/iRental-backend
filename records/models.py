from django.db import models
from users.models import User


class RentalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
