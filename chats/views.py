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
        print("user",user)
        try :
                messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('thread_name','-timestamp').distinct('thread_name')
              
                print("messages",messages)
                serializer=MessageSerializer(instance=messages,many=True)


                return Response(serializer.data, status=status.HTTP_200_OK)



            
        
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class Previouschat(APIView):
    def get(self, request, *args, **kwargs):
        
       
        other_user_id = self.kwargs.get('otherUserId')
        current_user=self.kwargs.get('currentUserId')
        # # check_out_date = self.kwargs.get('checkoutdate').strip()
        # # room_qty = self.kwargs.get('roomqty')

        # user=CustomUser.objects.get(id=otherUserId)
        # receiver=CustomUser.objects.get(id=currentUserId)
        print("receiver07777777777",other_user_id,current_user)
        try :

                room_name = "chat_"+(
                f"{current_user}_{other_user_id}"
                if int(current_user) > int(other_user_id)
                else f"{other_user_id}_{current_user}"
                )
                print("room_name",room_name)
                messages = Message.objects.filter(thread_name=room_name )
                print("messages",messages)
                serializer=MessageSerializer(instance=messages,many=True)


                return Response(serializer.data, status=status.HTTP_200_OK)



            
        
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)




class Chatlistpartner(APIView):
    def get(self, request, *args, **kwargs):
        
       
        user_id = self.kwargs.get('user_id')
        # # check_out_date = self.kwargs.get('checkoutdate').strip()
        # # room_qty = self.kwargs.get('roomqty')

        user=CustomUser.objects.get(id=user_id)
        print("user",user)
        try :
                messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('sender', '-timestamp').distinct('sender')
                print("messages",messages)
                serializer=MessageSerializer(instance=messages,many=True)


                return Response(serializer.data, status=status.HTTP_200_OK)



            
        
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class Fetch_userobj(APIView):
     def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('otherUserId1')
        print("jjjjjj",user_id)
        user=PartnerProfile.objects.get(id=user_id)
        print("userpartner",user)
        user_obj=CustomUser.objects.get(user=user)
        print("usert_obj",user_obj)
        response=user_obj.id
        return Response(response,status.HTTP_200_OK)



