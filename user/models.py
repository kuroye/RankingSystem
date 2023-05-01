from django.db import models
from school.models import School
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.hashers import make_password
# Create your models here.

class User(models.Model):

    POSITION = [
        ('S', 'School Student'),
        ('T', 'Teacher'),
        ('P', 'Parent'),
        ('U', 'Graduate')
    ]
    email = models.CharField(max_length=254, unique=True)
    fullname = models.CharField(max_length=128)
    password = models.CharField(max_length=254)
    position = models.CharField(max_length=1, choices=POSITION)

    def __str__(self):
        return self.fullname + ' ' + self.email


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    '''Пайдаланушыны сақтамас бұрын құпия сөзді шифрлау'''
    # pbkdf2_sha256$
    if not instance.password.startswith('pbkdf2_sha256$'):
        instance.password = make_password(instance.password)





class Notification(models.Model):

    content = models.TextField(null=True)

    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

class Subscription(models.Model):

    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)


