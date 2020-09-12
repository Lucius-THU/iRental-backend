from django.db import models
import bcrypt
from common import modeltodict


# password is saved as a hash

class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.BinaryField()
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=255, default='')
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

    def ingroup(self, group):
        groups = []
        for v in ['admin', 'provider', 'user']:
            groups.append(v)
            if group == v:
                return self.group in groups
        return False

    def isprovider(self):
        return self.ingroup('provider')

    def isadmin(self):
        return self.ingroup('admin')

    def todict(self, notifications=False):
        d = modeltodict(self, exclude='password')
        if notifications:
            a = []
            for item in self.notification_set.filter(unread=True):
                a.append({
                    'id': item.id,
                    'content': item.content
                })
            d['notifications'] = a
        return d


class SignupRequest(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=255)
    expire_at = models.DateTimeField()
