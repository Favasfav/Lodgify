
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('api/', include('accounts.api.urls')),
     path('admin/', admin.site.urls),
     path('partner/', include('partner.urls')),
     path('booking/', include('booking.urls')),
     path('chats/', include('chats.urls')),
     path('apirazorpay/', include('booking.apirazorpay.urls')),
    path("chat/", include("chats.urls")),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)