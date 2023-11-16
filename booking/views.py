from django.shortcuts import render
from rest_framework import serializers,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from partner.models import RoomProperty, RoomCategory, RoomAmenity, RoomPhoto
from .serializer import *
from .models import *
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Sum
import json
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from accounts.models import *

# Create your views here.
class Checkroomavailblity(APIView):
    def post(self, request, *args, **kwargs):
        property_id = self.kwargs.get('propertyId')
        check_in_date = self.kwargs.get('checkindate').strip()
        check_out_date = self.kwargs.get('checkoutdate').strip()
        room_qty = self.kwargs.get('roomqty')


        try:
            property = RoomProperty.objects.get(id=property_id)
            if property and check_out_date and check_in_date and room_qty:
                overlapping_bookings = Booking.objects.filter(
                    room=property,
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date
                )

                total_rooms_available = property.total_rooms
                total_rooms_booked = sum(booking.room_qty_booked for booking in overlapping_bookings)
                remaining_rooms = total_rooms_available - total_rooms_booked

                if remaining_rooms < int(room_qty):
                    return Response({"message": "Required quantity of rooms not available now"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "Book for these dates"}, status=status.HTTP_200_OK)



            return Response({"message": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)
        except RoomProperty.DoesNotExist:
            return Response({"message": "Invalid property ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


# # class Roombooking(APIView):

#     def post(self,request,*args,**kwargs):
#         property_id = self.kwargs.get('propertyId')
#         check_in_date = self.kwargs.get('checkindate').strip()
#         check_out_date = self.kwargs.get('checkoutdate').strip()
#         room_qty=self.kwargs.get('roomqty')
#         user_id=self.kwargs.get('user_id')
        
#         print("hhhhhhhhhh",request.data)
#         # data={
#         #     property_id:property_id,
#         #     check_in_date:check_in_date,
#         #     check_out_date:check_out_date,
#         #     user:user_id

#         # }
#         # serializer=BookingSerializer(data=data)

#         # if serializer.data.is_valid()
#         property = RoomProperty.objects.get(id=property_id)
#         customuser_obj=CustomUser.objects.get(id=user_id)
#         user=UserProfile.objects.get(user=customuser_obj)
        
#         print("property",property)
#         print("dataaaaaa------------------", property_id, check_out_date, check_in_date,room_qty)
#         try:
#               property = RoomProperty.objects.get(id=property_id)
#               if property and check_out_date and check_in_date and room_qty:
#                 overlapping_bookings = Booking.objects.filter(
#                     room=property,
#                     check_in_date__lt=check_out_date,
#                     check_out_date__gt=check_in_date
#                 )

#                 total_rooms_available = property.total_rooms
#                 total_rooms_booked = sum(booking.room_qty_booked for booking in overlapping_bookings)
#                 remaining_rooms = total_rooms_available - total_rooms_booked

#                 if remaining_rooms < int(room_qty):
#                     return Response({"message": "Required quantity of rooms not available now"}, status=status.HTTP_400_BAD_REQUEST)
                
                
                   
#                 else:
#                      total_amount=property.single_room_price*room_qty
#                      bookingobj=Booking(
#                             room=property,
#                             user=user,
#                             check_in_date=check_in_date,
#                             check_out_date=check_out_date,
#                             room_qty_booked=room_qty,
#                             total_amount=total_amount,


#                         )
#                      bookingobj.save()    

#                      Transcation(
#                         booking = bookingobj,
#                         user = user,
#                         partner = property.partner,
#                         partner_share = 0.7*float(total_amount),
#                         company_share = 0.3*float(total_amount),
                        
                        
                       
#                      )   .save()
#                      return Response({"message": " booked for these dates "}, status=status.HTTP_200_OK)            
                
#         except Exception as e:
#             print(e)
#             return Response({"message":"Something Wrong"},status=status.HTTP_400_BAD_REQUEST)  



class Bookinglist(APIView):
    def get(self,request,*args,**kwargs):

        user_id=self.kwargs.get('user_id')
        print("user_id",user_id)
        custom_obj=CustomUser.objects.get(id=user_id)
        user=UserProfile.objects.get(user=custom_obj)
        bookings=Booking.objects.filter(user=user)
        print("bookings",bookings)
        serializer=BookingSerializer(instance=bookings,many=True)   
        data=serializer.data
        print("hlllllllll",data)
        return Response(data,status=status.HTTP_200_OK)




       
class CancelOrder(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        order_id = request.data.get('booking_id')
        print(order_id, "order_id")

        booking = get_object_or_404(Booking, id=order_id)
        print("booking", booking)

       
        wallet, created = Wallet.objects.get_or_create(user=booking.user)

        
        wallet.balance += booking.total_amount
        print(wallet.balance, "ggggggggggg")
        wallet.save()
        booking.is_cancelled=True
        booking.save()
        return Response({'message': 'Order canceled successfully.'}, status=status.HTTP_200_OK)


class Bookingall(APIView):
    def get(self,request, *args, **kwargs):
        booking=Booking.objects.all()
        data=booking
        print("booking",booking)
        serializer=BookingSerializer(instance=booking,many=True)
        if serializer:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)    
class Totalrevenue(APIView):
    def get(self,request, *args, **kwargs):
        # booking=Booking.objects.filter(is_cancelled=False)
        # data=booking.total_amount
        total_amount_aggregation = Booking.objects.filter(is_cancelled=False).aggregate(total_amount_sum=Sum('total_amount'))


        total_amount_sum = total_amount_aggregation.get('total_amount_sum', 0)
        print("total sum",total_amount_sum)
        
        if total_amount_sum:
            return Response(total_amount_sum,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)    
