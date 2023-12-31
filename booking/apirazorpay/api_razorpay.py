from rest_framework.views import APIView
from rest_framework import status
from booking.apirazorpay.razorpay_serializer import CreateOrderSerializer,TranscationModelSerializer,TransactioncharcheckSerializer
from rest_framework.response import Response
from accounts.views import  *

from booking.models import *
from booking.apirazorpay.razorpay.main import RazorpayClient
rz_client=RazorpayClient()
from datetime import datetime
class CreateOrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            
            property_id = self.kwargs.get('propertyId')
            check_in_date_str = self.kwargs.get('checkindate').strip()
            check_out_date_str = self.kwargs.get('checkoutdate').strip()
            room_qty = self.kwargs.get('roomqty')
            user_id = self.kwargs.get('user_id')

            property = RoomProperty.objects.get(id=property_id)
            customuser_obj = CustomUser.objects.get(id=user_id)
            user = UserProfile.objects.get(user=customuser_obj)
            
            block_obj = Blockbooking.objects.filter(property=property)

            if block_obj:
                for i in block_obj:
                    check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
                    check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()
                    if i.end_date >= check_in_date and check_out_date >= i.starting_date:
                        return Response({"message": "Required quantity of rooms not available for the dates"},
                                        status=status.HTTP_400_BAD_REQUEST)

            if property and check_out_date_str and check_in_date_str and room_qty:
                check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()
                print("hiii",property)
                overlapping_bookings = Booking.objects.filter(
                    room=property,
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date,
                    is_cancelled=False,
                    
                )
                print("hiii",property,overlapping_bookings)
                if overlapping_bookings:
                    total_rooms_available = property.total_rooms
                    total_rooms_booked = sum(booking.room_qty_booked for booking in overlapping_bookings)
                    remaining_rooms = total_rooms_available - total_rooms_booked

                    if remaining_rooms < int(room_qty):
                        return Response({"message": "Required quantity of rooms not available for the date "},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        create_order_serializer = CreateOrderSerializer(data=request.data)

                        if create_order_serializer.is_valid():
                            amount = create_order_serializer.validated_data.get("amount")
                            currency = create_order_serializer.validated_data.get("currency")

                            order_response = rz_client.create_order(
                                    amount=amount,
                                    currency=currency
                                )
                            print("order_response===============>",order_response)
                        
                            response = {
                                "status_code": status.HTTP_201_CREATED,
                                "message": "order_created",
                                "data": order_response
                            }
                        else:
                            response = {
                                "status_code": status.HTTP_400_BAD_REQUEST,
                                "message": "bad request",
                                "error": create_order_serializer.errors
                            }

                else:
                    create_order_serializer = CreateOrderSerializer(data=request.data)

                    if create_order_serializer.is_valid():
                        amount = create_order_serializer.validated_data.get("amount")
                        currency = create_order_serializer.validated_data.get("currency")
                        print("amount",amount,currency)
                        order_response = rz_client.create_order(
                            amount=amount,
                            currency=currency
                        )
                        print("order_response========================>>>",order_response)
                        # if 'order_id' not in order_response or 'payment_id' not in order_response:
                        #      return Response({"message": "Invalid response from Razorpay API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
            
                        response = {
                            "status_code": status.HTTP_201_CREATED,
                            "message": "order_created",
                            "data": order_response
                        }
                        
                    if not create_order_serializer.is_valid():
                        print("Validation Errors:", create_order_serializer.errors)
                        response = {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "message": "bad request",
                            "error": create_order_serializer.errors
                        }
                        return Response(response)


                return Response(response)

        except Exception as e:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
  

class TranscationAPIView(APIView):
    def post(self,request,*args,**kwargs):
        checkin=[]
        checkout=[]
        property_id = self.kwargs.get('propertyId')
        check_in_date = self.kwargs.get('checkindate').strip()
        check_out_date = self.kwargs.get('checkoutdate').strip()
        room_qty=self.kwargs.get('roomqty')
        user_id=self.kwargs.get('user_id')
        property = RoomProperty.objects.get(id=property_id)
        customuser_obj=CustomUser.objects.get(id=user_id)
        user=UserProfile.objects.get(user=customuser_obj)
        checkin=check_in_date.split('-')
        print(checkin[2])
        checkout=check_out_date.split('-')
        print(checkout[2])
        no_ofdays=int(checkout[2])-int(checkin[2])+1
        print("no_ofdays",no_ofdays)
        data=request.data
        print("dataTranscationAPIView",data)
        razorpay_order_id=data.get("order_id")
        razorpay_payment_id=data.get("payment_id")
        razorpay_signature=data.get("signature")
        # razorpay_amount=data.get("amount")
        data={
             "order_id":razorpay_order_id,
            "payment_id":razorpay_payment_id,
            "signature":razorpay_signature,
             "user":user,
            # "partner":property.partner,
            }
        serializer=TransactioncharcheckSerializer(data=data)
        
        if serializer.is_valid():
            print("data===================",razorpay_order_id,razorpay_payment_id,razorpay_signature)
            is_status= rz_client.verify_payment(
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature,
            )
            if is_status:
                            print("hloo")

                            total_amount=property.single_room_price*room_qty*no_ofdays
                            bookingobj=Booking(
                                    room=property,
                                    user=user,
                                    check_in_date=check_in_date,
                                    check_out_date=check_out_date,
                                    room_qty_booked=room_qty,
                                    total_amount=total_amount,


                                )
                            bookingobj.save()    
                            test(request,user_id,check_out_date)
                            Transcation(
                                booking = bookingobj,
                                user = user,
                                partner = property.partner,
                                partner_share = 0.7*float(total_amount),
                                company_share = 0.3*float(total_amount),
                                signature=razorpay_signature,
                                payment_id=razorpay_payment_id,
                                order_id=razorpay_order_id,
                                
                                
                            
                
                            )   .save()


                          

                           
                # except:
                #      response={
                #     "status_code":status.HTTP_400_BAD_REQUEST,
                #     "message":"bad request",
                #     "error":TranscationModelSerializer.errors
                #     }
                # return Response(response,status=status.HTTP_400_BAD_REQUEST)





                            response={
                                                "status_code":status.HTTP_201_CREATED,
                                                "message":"order_created",
                                                

                                            }


                    
                            return Response(response,status=status.HTTP_201_CREATED)
        else:
            response={
                "status_code":status.HTTP_400_BAD_REQUEST,
                "message":"bad request",
                "error":TranscationModelSerializer.errors
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)