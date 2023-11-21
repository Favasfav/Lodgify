from django.shortcuts import render
from rest_framework import serializers,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from accounts.models import *
from django.db.models import Q
# Create your views here.
class Chatlist(APIView):
    def get(self, request, *args, **kwargs):
        
       
        user_id = self.kwargs.get('user_id')
        # # check_out_date = self.kwargs.get('checkoutdate').strip()
        # # room_qty = self.kwargs.get('roomqty')

        user=CustomUser.objects.get(id=user_id)
        try :
                messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('receiver', '-timestamp').distinct('receiver')
                print("messages",messages)
                serializer=MessageSerializer(instance=messages,many=True)


                return Response(serializer.data, status=status.HTTP_200_OK)



            
        
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    