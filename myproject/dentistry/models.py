from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager

class Role(models.Model):
    name = models.CharField(max_length=255)

class Profession(models.Model):
    name = models.CharField(max_length=255)

class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=1)
    profession = models.ForeignKey(Profession, on_delete=models.PROTECT, default=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'patronymic', 'phone']

    class Meta:
        abstract = False


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()


class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class Reception(models.Model):
    data_time = models.DateTimeField()
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.PROTECT, null=True)
    users = models.ManyToManyField(User)


class Review(models.Model):
    comment = models.CharField(max_length=255)
    date = models.DateField()
    reception = models.ForeignKey(Reception, on_delete=models.PROTECT)
