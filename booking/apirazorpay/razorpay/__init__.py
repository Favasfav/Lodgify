import razorpay
from django.conf import settings
client = razorpay.Client(auth=("rzp_test_GlidMFhzhQAugp", "cVJgnrW2HlTuFN9lvJzWpJWh"))

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))