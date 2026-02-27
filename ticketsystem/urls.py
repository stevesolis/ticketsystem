from django.contrib import admin
from django.urls import path, include

urlpatterns = [ //Holi
    path('admin/', admin.site.urls),
    path('', include('boletos.urls')),
]