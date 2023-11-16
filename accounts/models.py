   
from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('partner', 'partner'),
        ('admin', 'admin'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=False)
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username','role','phone_no']
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    phone_no = models.CharField(max_length=30, unique=True, blank=True, null=True)
    is_blocked=models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='image_profiles/',blank=True, null=True)
    def _str_(self): 
        return  self.email 
       

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='userprofile')
    
    
    # is_blocked=models.BooleanField(default=False)
    

    def _str_(self):
        return self.user 
    

class PartnerProfile(models.Model):
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
     

     def _str_(self):
        return self.user
     

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   

    def _str_(self):
        return self.user.email



class Wallet(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


