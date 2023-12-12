# import razorpay
from django.conf import settings
import os
import razorpay
# client = razorpay.Client(auth=("rzp_test_5xVEgUg2MnBlyx","WQx9vzmp4XoZDMgX5Cw6pRLS"))

client = razorpay.Client(auth=(os.getenv('RAZORPAY_KEY_ID1'), os.getenv('RAZORPAY_SECRET_KEY1'))) 