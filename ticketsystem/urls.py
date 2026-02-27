from django.contrib import admin
from django.urls import path
from boletos.views import home, admin_redirect


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]