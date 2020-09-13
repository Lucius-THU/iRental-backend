from django.db import models
from users.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    @classmethod
    def create(cls, user, content):
        if content is None:
            return None
        return cls.objects.create(**{
            'user': user,
            'content': content,
            'unread': True
        })
