from rest_framework import serializers,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RoomProperty, RoomCategory, RoomAmenity, RoomPhoto
from .serializer import *
from .models import *
from django.http import JsonResponse
from django.core import serializers
from .models import RoomProperty
import json
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from booking.models import *
from rest_framework.permissions import IsAuthenticated

class Addproperty(APIView):
   
    def post(self, request):
        data = request.data
        print("data", data)
        serializer=PropertySerializer(data=data)
        if serializer.is_valid():
            
          try:
            print("hhhhhhhhhhhhhhhh")
            partner = PartnerProfile.objects.get(id=data['partner'])
            
            print("hhhhhhhhhhhhhhhh",partner.user)
           
            

            # Create a RoomProperty instance
            room_property = RoomProperty(
                
                property_type=data.get("property_type"),
                property_name=data.get("property_name"),
                total_rooms=data.get("total_rooms"),
                single_room_price=data.get("single_room_price"),
                adults_price=data.get("adults_price"),
                total_room_price=data.get("total_room_price"),
                capacity=data.get("capacity"),
                property_address=data.get("property_address"),
                city=data.get("city"),
                state=data.get("state"),
                zip_code=data.get("zip_code"),
                parking=data.get("parking"),
                swimming_pool=data.get("swimming_pool"),
                room_description=data.get("room_description"),
                maplocation=data.get("maplocation"),
                country=data.get("country"),
                is_verified=False,  # Set to False by default
                partner=partner,
            )
            print("room_property",room_property)
           
            room_property.save()


            
            amenities = data.getlist("amenities")
            print("ame-----------",amenities)
            for amenity in amenities:
                amenities_list=RoomAmenity(amenities=amenity,room_property=room_property)
                amenities_list.save()

            photos=data.getlist("photos")
            for i  in photos:
                photo_list=RoomPhoto(photo=i,room_property=room_property)    
                photo_list.save()

            category=data.get("category") 
            
            category_list=RoomCategory(category=category,room_property=room_property)    
            category_list.save()

            

            return Response({"message": "Property created successfully"}, status=status.HTTP_201_CREATED)
          except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error":""}, status=status.HTTP_400_BAD_REQUEST)
        


class Propertylist(APIView) :

    def get(self, request):

        print("request.headers=========",request.headers)

        if request.method == 'GET':
        
                data = RoomProperty.objects.all()
                
                serializer = PropertySerializer(data, many=True)
                
        
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class Verifyproperty(APIView):
    def post(self,request,property_id):
        print(property_id)
        property=RoomProperty.objects.get(id=property_id)
        print(property.is_verified)
        property.is_verified= not property.is_verified
        property.save()
        print(property.is_verified)
        return Response({"message": "Property verified successfully"}, status=status.HTTP_201_CREATED)




class Propertyview(RetrieveAPIView):
    queryset = RoomProperty.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'property_id'  

    def get_object(self):
        
        property_id = self.kwargs['property_id']

        
        return RoomProperty.objects.get(id=property_id)


class PropertyListView(APIView):
    
    
   
    def get(self, request):
        print("request",request.headers)
        # print("hiiiiiiii",request.data)
        print("hhhh",request.headers)

        if request.method == 'GET':
            
        
                data1 = RoomProperty.objects.all()
                data=data1.filter(is_verified=True)
                serializer = PropertySerializer(data, many=True)
               
        
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
class PartnerProperty(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, partner_id):
        print("hiii",partner_id)
       

        if request.method == 'GET':
            data = RoomProperty.objects.filter(partner_id=partner_id)
            serializer = PropertySerializer(data, many=True)
            

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Updateproperty(generics.RetrieveUpdateDestroyAPIView):
    queryset=RoomProperty.objects.all()
    serializer_class=PropertySerializer




class Getpropertybylocation(APIView):
    def get(self, request, *args, **kwargs):
        print("request---------",request.headers)
        maplocation = self.kwargs.get('location', '')
        category = request.query_params.getlist('category', [])
        amenities = request.query_params.getlist('amenities', [])
        property_type = request.query_params.getlist('Property_Type', [])
        print("category",category)
        print("amenities",amenities)
        print("property_type",property_type)
        queryset = RoomProperty.objects.all()
        if maplocation:
            queryset = queryset.filter(maplocation=maplocation)
        # property_type = ['Resort','Hotel']    
        if property_type: 
            
            
            queryset=queryset.filter(property_type__in=property_type)
        

        if category:
            queryset= queryset.filter(category__category__in=category) 


        if amenities:
            
           
            queryset=queryset.filter(amenities__amenities__in=amenities)
            print("queryset",queryset)
        
        
        serializer = PropertySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)





