from django.db import models
from django.contrib.auth.models import AbstractBaseUser

#Identifier is e-mail instead of user ID
class User(AbstractBaseUser):
    username = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField()

    REQUIRED_FIELDS = ['username', 'email', 'password']

    def __unicode__(self):
        return self.username
        
class Dotfile(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    