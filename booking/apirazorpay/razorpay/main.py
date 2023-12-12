from .import client
from rest_framework.serializers import ValidationError
from rest_framework import status
import os

class RazorpayClient:
    def create_order(self,amount,currency):
        data={
            "amount":amount,
            "currency":currency,

        }
      
        try:
            
            order_data=client.order.create(data=data)
            print("hhghggug====================",order_data)
            return order_data
        except Exception as e:
            raise ValidationError(
                {
            "status_code" :status.HTTP_400_BAD_REQUEST,
            "message":str(e)
            }  
            )
  
    def verify_payment(self,razorpay_order_id,razorpay_payment_id,razorpay_signature):
        
        # try:
        #    print("verify_payment",razorpay_order_id,razorpay_payment_id,razorpay_signature)
        #    return client.utility.verify_payment_signature({
        #     'razorpay_order_id': razorpay_order_id,
        #     'razorpay_payment_id': razorpay_payment_id,
        #     'razorpay_signature': razorpay_signature
        #     })
               
        # except Exception as e:
        #     print("error",e)
        #     raise ValidationError({
        #         "status_code":status.HTTP_400_BAD_REQUEST,
        #         "message":e
        #     })     
        return True