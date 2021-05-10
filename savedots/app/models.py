from django.db import models


class User(models.Model):
    username = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField()
    
class Dotfile(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    