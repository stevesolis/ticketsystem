from django.http import HttpResponse
from django.shortcuts import render

def validar_boleto(request):
    return HttpResponse("Validación de boleto funcionando correctamente")