from django.db import models
from school.models import School
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


POSITION = [
        ('S', 'School Student'),
        ('T', 'Teacher'),
        ('P', 'Parent'),
    ]

class User(AbstractUser):

    position = models.CharField(max_length=1, choices=POSITION)
    email = models.CharField(max_length=254, unique=True, blank=False, null=False)
    school = models.OneToOneField(School, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username + ' ' + self.email




class Notification(models.Model):

    content = models.TextField(null=True)

    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

class Subscription(models.Model):

    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)


