from django.db import models
from accounts.models import PartnerProfile





class RoomProperty(models.Model):
    PROPERTY_TYPES = (
        ('Hotel', 'Hotel'),
        ('Resort', 'Resort'),
    )
    partner = models.ForeignKey(PartnerProfile, on_delete=models.CASCADE)

   
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    total_rooms = models.PositiveIntegerField()
    single_room_price = models.DecimalField(max_digits=10, decimal_places=2)
    adults_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_room_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    property_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    parking = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    room_description = models.TextField()
    property_name = models.TextField(max_length=50, blank=True, null=True, default='')
    maplocation = models.CharField(max_length=110)
    is_verified=models.BooleanField(default=False)
    country=models.CharField(max_length=100,default='INDIA')


    def __str__(self):
        return self.property_name
    
    
class RoomPhoto(models.Model):
    room_property = models.ForeignKey(RoomProperty, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='room_photos/')

    def __str__(self):
        return f'Photo of {self.room_property.property_type} Property'

class RoomCategory(models.Model):
    CATEGORY_CHOICES = [
        ('1_star', '1 Star'),
        ('3_stars', '3 Stars'),
        ('4_stars', '4 Stars'),
        ('deluxe_premium_luxury', 'Deluxe/Premium/Luxury'),
    ]

    room_property = models.ForeignKey(RoomProperty, on_delete=models.CASCADE, related_name='category')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.category

class RoomAmenity(models.Model):
    AMENITY_CHOICES = [
        ('power_backup', 'Power Backup'),
        ('ac', 'AC'),
        ('fire_extinguisher', 'Fire Extinguisher'),
        ('wifi', 'WiFi'),
        ('daily_house_keeping', 'Daily House Keeping'),
        ('attached_bathroom', 'Attached Bathroom'),
        ('first_aid_kit', 'First Aid Kit'),
        ('tv', 'TV'),
        ('air_conditioner', 'Air Conditioner'),
    ]

    room_property = models.ForeignKey(RoomProperty, on_delete=models.CASCADE, related_name='amenities')
    amenities = models.CharField(max_length=50, choices=AMENITY_CHOICES)

    def __str__(self):
        return self.amenities
    

