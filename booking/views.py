from django.shortcuts import render
from rest_framework import serializers,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from partner.models import RoomProperty, RoomCategory, RoomAmenity, RoomPhoto,Blockbooking
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
from rest_framework.decorators import permission_classes
from accounts.permissions import *
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
class Checkroomavailblity(APIView):
    permission_classes=[IsAuthenticated,Userpermission]
    def post(self, request, *args, **kwargs):
        property_id = self.kwargs.get('propertyId')
        check_in_date_str = self.kwargs.get('checkindate').strip()
        check_out_date_str = self.kwargs.get('checkoutdate').strip()
        room_qty = self.kwargs.get('roomqty')

        try:
            property = RoomProperty.objects.get(id=property_id)
            if property and check_out_date_str and check_in_date_str and room_qty:
                check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

                overlapping_bookings = Booking.objects.filter(
                    room=property,
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date,
                    is_cancelled=False,
                ) 
                print("overlaped",overlapping_bookings)
                block_obj = Blockbooking.objects.filter(property=property)
                print("block_obj", block_obj)
                if block_obj:
                    for i in block_obj:
                       print(i.end_date,i.starting_date) 
                       if  i.end_date>=check_in_date and check_out_date >=i.starting_date:
                        return Response({"message": "Required quantity of rooms not available for current Time"}, status=status.HTTP_400_BAD_REQUEST)

                
                total_rooms_available = property.total_rooms
                print("total_rooms_available",total_rooms_available)
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


class Bookinglist(APIView):
    
    permission_classes=[IsAuthenticated,Userpermission]
    def get(self,request,*args,**kwargs):
        print(request)
        print("Headers:", request.headers)
        print("Token:", request.headers.get('Authorization'))

        user_id=self.kwargs.get('user_id')
        print("user_id--------------",user_id)
        custom_obj=CustomUser.objects.get(id=user_id)
        user=UserProfile.objects.get(user=custom_obj)
        print("user",user)
        bookings=Booking.objects.filter(user=user)
        
        serializer=BookingSerializer(instance=bookings,many=True)   
        data=serializer.data
      
        return Response(data,status=status.HTTP_200_OK)





class Bookinglistlatestadmin(APIView):
    def get(self, request):
        try:
            bookings = Booking.objects.all().order_by('-id')[:5]
            print("bookings", bookings)
            serializer = BookingSerializer(instance=bookings, many=True)

            if serializer:
                data = serializer.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

permission_classes=[IsAuthenticated,Userpermission]       
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
        transaction=Transcation.objects.get(booking=booking)
        transaction.partner_share=transaction.partner_share-int(booking.total_amount*0.7)
        
        transaction.company_share=transaction.company_share-int(booking.total_amount*0.3)
        print("transaction.company_share",transaction.company_share)
        transaction.save()
        print("transaction",transaction)
        booking.save()
        return Response({'message': 'Order canceled successfully.'}, status=status.HTTP_200_OK)


class Bookingall(APIView):
    permission_classes=[IsAuthenticated,AdminPermission]
    def get(self,request, *args, **kwargs):
        booking=Booking.objects.all()
        data=booking
        
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





class GetpartnerRevenue(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('partner_id')
        user_obj=CustomUser.objects.get(id=user_id)
        partner_obj=PartnerProfile.objects.get(user=user_obj)
       
       
        print(partner_obj,"fff")
        transaction_obj = Transcation.objects.filter(partner=partner_obj)
        print("transaction_obj",transaction_obj)
        
        partner_revenue = transaction_obj.aggregate(Sum("partner_share", default=0))
        
        print(partner_revenue, "pppppppppppppppp")
        
        # Access the specific field from the aggregation result
        partner_revenue_sum = partner_revenue.get('partner_share__sum', 0)
       
        if partner_revenue_sum:
            
            response_data =  partner_revenue_sum
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data=0
            return Response(response_data, status=status.HTTP_200_OK)
      
class Bookinglatest(APIView):
    def get(self,request, *args, **kwargs):
        booking=Booking.objects.all().order_by('-id')[:5]
        data=booking
        print("booking",booking)
        serializer=BookingSerializer(instance=booking,many=True)
        if serializer:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)  
    
class BookingTotalpartner(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        user = CustomUser.objects.get(id=user_id)

        try:
            partner = PartnerProfile.objects.get(user=user)
            rooms = RoomProperty.objects.filter(partner=partner)

            if rooms:
                booking_no = Booking.objects.filter(room__in=rooms)
                print("booking_no", booking_no)
                serializer=BookingSerializer(instance=booking_no,many=True)

                if serializer:
                    data=serializer.data
                    return Response(data, status=status.HTTP_200_OK)
                    
                else:
                   
                    return Response([], status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class Bookingtotalnopartner(APIView):
    def get(self, request, *args, **kwargs):
        
        user_id=self.kwargs.get("user_id") 
        user=CustomUser.objects.get(id=user_id)
        print("user",user)
        try:
            
            partner=PartnerProfile.objects.get(user=user)
           
            rooms=RoomProperty.objects.filter(partner=partner)
            
            booking_no=0
            if rooms:
                print("ggggg0000000")
                try:
                    booking_no = Booking.objects.filter(room__in=rooms).count()
                    
                    print("booking_nooo", booking_no)
                
                    if booking_no:
                        return Response(booking_no, status=status.HTTP_200_OK)
                    
                        
                except:
                        booking_no=0
                        return Response(booking_no, status=status.HTTP_200_OK)

        except Exception as e: 
            print(e)
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        



class Blockproperty(APIView):
    def post(self,request,*args,**kwargs):
        property_id=self.kwargs.get('property_id')
        print("property_id",property_id,"request.data",request.data) 
        property=RoomProperty.objects.get(id=property_id)
        end_date = request.data.get('enddate').strip()
        starting_date = request.data.get('startdate').strip()
        print("hhhhhhhhhh",starting_date,end_date,property)
        try:
            if request.data and property_id:
                print("jjjjjjjjjjj")
                abc=Blockbooking(
                    end_date=end_date,
                    property=property,
                    starting_date=starting_date,


                )
                
                abc.save()
                print("ooooooooooooooooooooo",abc)

                return Response(status.HTTP_200_OK)    
            return Response(status.HTTP_400_BAD_REQUEST)    
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
        
class Bookingreport(APIView):
            def get(self,request):
                try:
                    
                        cancelled_obj_count=Booking.objects.filter(is_cancelled=True).count()
                        confirem_obj_count=Booking.objects.all().count()-cancelled_obj_count
                        data={
                           "cancelled_obj_count":cancelled_obj_count,
                           "confirem_obj_count":confirem_obj_count

                        }
                        return Response(data,status=status.HTTP_200_OK)
                    # return Response(data={cancelled_obj_count:0,confirem_obj_count:0},status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class Bookinglatestpartner(APIView):
    def get(self, request, *args, **kwargs):
        
        user_id=self.kwargs.get("user_id") 
        user=CustomUser.objects.get(id=user_id)
        print("user",user)
        try:
            
            partner=PartnerProfile.objects.get(user=user)
           
            rooms=RoomProperty.objects.filter(partner=partner)
            
            print("rooms",rooms)
            if rooms:
                print("ggggg")
                try:
                        booking = Booking.objects.filter(room__in=rooms)[:5]
                        serializer=BookingSerializer(instance=booking,many=True)
                        if serializer:
                            data=serializer.data
                            return Response(data, status=status.HTTP_200_OK)
                        
                            
                except:  
                          booking=0
                          return Response([], status=status.HTTP_200_OK)      
                
                
            else:
                booking=0
                return Response(booking, status=status.HTTP_200_OK)

        except Exception as e:  
            print(e)
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
