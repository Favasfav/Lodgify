from django.urls import path

from .views import *
urlpatterns=[
     path('Addproperty/', Addproperty.as_view(), name='Addproperty'),
     path('propertylist/', Propertylist.as_view(), name='propertylist'),
     path('Verifypropertyaproval/<int:property_id>/', Verifyproperty.as_view(), name='Verifypropertyaproval'),
     path('propertyview/<int:property_id>/', Propertyview.as_view(), name='propertyview'),
     path('propertylistview', PropertyListView.as_view(), name='propertylistview'),
     path('Partnerproperties/<int:partner_id>/', PartnerProperty.as_view(), name='PartnerProperty'),
     path('updateproperty/<int:pk>/', Updateproperty.as_view(), name='updateproperty'), 
     path('getpropertybylocation/<str:location>/', Getpropertybylocation.as_view(), name='getpropertybylocation'), 
    
]