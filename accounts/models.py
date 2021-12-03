from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self,email,password,**other_fields):

        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)


        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        user = self.create_user(email,password,**other_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_user(self,email,password,**other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must provide an email id'))

        email = self.normalize_email(email)
        user  = self.model(email=email,**other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(gettext_lazy('email address'),unique=True)
    username = models.CharField(max_length=50, blank=True ,null=True,unique=True)
    creation_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)


    objects = CustomAccountManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return "@{}".format(self.email)
