from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wallet.models import Wallet
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self,email,password,**extra):
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        if extra.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email,password,**extra)
    
class User(AbstractUser):
    username=models.CharField(max_length=150,unique=False)
    email=models.EmailField(unique=True)
    ROLE_CHOICES=[
        ('customer','Customer'),
        ('seller','Seller')
    ]
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='customer')
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=UserManager() # type: ignore


class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    contact_phone=models.CharField(max_length=15,blank=True,null=True)
    preferences=models.TextField(blank=True,null=True)

   

@receiver(post_save,sender=User)
def create_stuff(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(user=instance)