from django.contrib import admin
from django.urls import path, include
#Holis
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('boletos.urls')),
]