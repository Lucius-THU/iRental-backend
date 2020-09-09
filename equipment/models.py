from django.db import models
from users.models import User


class Equipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    expire = models.DateTimeField()
    launched = models.BooleanField(default=False)
