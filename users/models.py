from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
