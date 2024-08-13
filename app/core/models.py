from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# from phonenumber_field.modelfields import PhoneNumberField
from.managers import CustomUserManager


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"),max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()


    def __str__(self):
        return self.email


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    link = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.title
