from django.db import models
import bcrypt


class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=255, default='')

    # password hash
    password = models.BinaryField()

    group = models.CharField(max_length=255, default='user')

    @classmethod
    def create(cls, email, password, **kwargs):
        pw = password.encode('utf-8')
        return cls.objects.create(**kwargs, **{
            'email': email,
            'password': bcrypt.hashpw(pw, bcrypt.gensalt())
        })

    @classmethod
    def from_session(cls, session):
        if session is None:
            return None
        pk = session.get_decoded()['user_id']
        return cls.objects.filter(pk=pk).first()

    def __str__(self):
        return self.email

    def authenticate(self, password):
        pw = password.encode('utf-8')
        return bcrypt.checkpw(pw, self.password)
