from django.http import HttpResponse
from django.shortcuts import redirect


def home(request):
    """
    Página principal pública del sistema.
    Puedes cambiarla luego por una plantilla HTML.
    """
    return HttpResponse("Sistema de boletos funcionando correctamente")


def admin_redirect(request):
    """
    Redirige al panel administrativo.
    Útil si quieres usarlo más adelante.
    """
    return redirect("/admin/")