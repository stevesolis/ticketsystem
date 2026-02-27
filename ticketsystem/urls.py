from django.http import HttpResponse
from django.urls import path, include

def home(request):
    return HttpResponse("Sistema de boletos funcionando correctamente")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]