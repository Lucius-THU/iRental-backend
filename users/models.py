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
    def load(cls, session):
        try:
            return cls.objects.get(pk=session['user_id'])
        except BaseException:
            return None

    def __str__(self):
        return self.email

    def authenticate(self, password):
        pw = password.encode('utf-8')
        return bcrypt.checkpw(pw, self.password)

    def in_group(self, group):
        groups = []
        for g in ['admin', 'provider', 'user']:
            groups.append(g)
            if group == g:
                return self.group in groups
        return False
