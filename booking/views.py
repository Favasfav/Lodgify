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


class Roombooking(APIView):
    def post(self,request,*args,**kwargs):
        property_id = self.kwargs.get('propertyId')
        check_in_date = self.kwargs.get('checkindate').strip()
        check_out_date = self.kwargs.get('checkoutdate').strip()
        room_qty=self.kwargs.get('roomqty')
        user_id=self.kwargs.get('user_id')
        
        print("hhhhhhhhhh",request.data)
        # data={
        #     property_id:property_id,
        #     check_in_date:check_in_date,
        #     check_out_date:check_out_date,
        #     user:user_id

        # }
        # serializer=BookingSerializer(data=data)

        # if serializer.data.is_valid()
        property = RoomProperty.objects.get(id=property_id)
        customuser_obj=CustomUser.objects.get(id=user_id)
        user=UserProfile.objects.get(user=customuser_obj)
        
        print("property",property)
        print("dataaaaaa------------------", property_id, check_out_date, check_in_date,room_qty)
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
                     total_amount=property.single_room_price*room_qty
                     bookingobj=Booking(
                            room=property,
                            user=user,
                            check_in_date=check_in_date,
                            check_out_date=check_out_date,
                            room_qty_booked=room_qty,
                            total_amount=total_amount,


                        )
                     bookingobj.save()    

                     Transcation(
                        booking = bookingobj,
                        user = user,
                        partner = property.partner,
                        partner_share = 0.7*float(total_amount),
                        company_share = 0.3*float(total_amount),
                        
                        
                       
                     )   .save()
                     return Response({"message": " booked for these dates "}, status=status.HTTP_200_OK)            
                
        except Exception as e:
            print(e)
            return Response({"message":"Something Wrong"},status=status.HTTP_400_BAD_REQUEST)         