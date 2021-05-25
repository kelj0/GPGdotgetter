import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        """
        Created user with given email username and password
        :param: email 
        :param: username
        :param: password
        """
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()
        return user
    
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    username = models.CharField(
        max_length=32, blank=False, null=False, unique=True
    )
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'username', 'password']

    def __str__(self):
        return f"{self.username} <{self.email}> "\
               f"{'active' if self.is_active else 'inactive'}"
