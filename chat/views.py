from django.shortcuts import render
from rest_framework import serializers,generics  
from rest_framework.views import APIView
# Create your views here.
from rest_framework.generics import ListAPIView
from .models import *
from .serializer import MessageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Subquery, Q   
from rest_framework import permissions
# class MyIndex(ListAPIView):
#     serializer_class = MessageSerializer
#     def  get_queryset(self):
#         user_id=self.kwargs['user_id'] 

#         # messages=ChatMessage.objects.filter(
#         #     id__in=Subquery(CustomUser.objects.filter(Q(sender__reciever=user_id)|Q(reciever__sender=user_id))
#         #     .annotate(last_msg=Subquery(
                
                
#         #         ChatMessage.objects.filter(
#         #         Q(sender=OuterRef('id'),reciever=user_id)|Q(reciever=OuterRef('id'),sender=user_id)
#         #     ).order_by("-id")[:1].value_list("id",flat=True)).value_list("last_msg",flat=True).order_by('-id'))).order_by('-id')
#         # )
#         messages=ChatMessage.objects.filter(sender=user_id)
#         return messages

# class MyIndex(ListAPIView):
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['user_id']

#         user=CustomUser.objects.filter(id=user_id)
#         # print(user,"user")
#         # userprofile=UserProfile.objects.filter(user_id=user_id)
#         # # Retrieve all messages where the sender is the specified user
#         # print(userprofile)
#         # id1=userprofile.id
#         # messages = ChatMessage.objects.filter(sender_id=id1)
#         # return messages
      
        

        
#         queryset = ChatMessage.objects.filter(
#             models.Q(sender=user) | models.Q(receiver=user)
#         )

#         return queryset




class MyIndex(generics.ListAPIView):
    serializer_class = MessageSerializer
    

    def get_queryset(self):
        
        
        user_id = self.kwargs['user_id']

        user=CustomUser.objects.get(id=user_id)
        current_user_profile =UserProfile.objects.get(user_id=user_id)

        
        queryset = ChatMessage.objects.filter(
            models.Q(sender=current_user_profile)
        )

        return queryset




class GetMessages(generics.ListAPIView):
    serializer_class=MessageSerializer     
    def get_queryset(self):
        sender_id=self.kwarg['sender_id']
        reciever_id=self.kwarg['reciever_id']
        messages=ChatMessage.objects.filter(sender__in=[sender_id,reciever_id],
        reciever__in=[sender_id,reciever_id])   

        return messages

# class  SendMessages(generics.CreateAPIView):
    
    
#     queryset = ChatMessage.objects.all()

#     parser_classes = (MultiPartParser, FormParser)
     
#     serializer_class=MessageSerializer

class SendMessages(APIView):
    def post(self, request):
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            try:
                sender_id = data.get('sender')
                receiver_id = data.get('receiver')
                user_id=data.get('user')
                print("Sender ID", sender_id, "Receiver ID",receiver_id)

                # Retrieve the sender and receiver instances
                sender = UserProfile.objects.get(id=sender_id)
                receiver = PartnerProfile.objects.get(id=receiver_id)
                user = CustomUser.objects.get(id=user_id)
                
                ChatMessage(
                    user=user,  
                    sender=sender,
                    reciever=receiver,  
                    message=data.get('message')
                ).save()
                return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
            except CustomUser.DoesNotExist:
                return Response({"error": "Sender or receiver not found"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 

         
  

    