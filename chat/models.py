from django.db import models
from accounts.models import *


class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user')
    sender=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='sender')
    reciever=models.ForeignKey(PartnerProfile,on_delete=models.CASCADE,related_name='reciever')
    message= models.TextField(max_length=200)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField( auto_now_add=True)


    class Meta:
        ordering=['date']
        verbose_name_plural='Message'


    def __str__(self):
        return f"{self.sender} -  {self.reciever}"      

    @property
    def sender_profile(self):
        sender_profile=UserProfile.objects.get(user=self.sender)
        return sender_profile   
    @property
    def reciever_profile(self):
        sender_profile=PartnerProfile.objects.get(user=self.sender)
        return sender_profile      

    
    
    