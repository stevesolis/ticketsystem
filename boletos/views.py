from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Boleto
@login_required

def validar_boleto(request, codigo):
    try:
        # 1. Buscamos el boleto. IMPORTANTE: El campo debe llamarse 'codigo' en tu modelo
        boleto = get_object_or_404(Boleto, codigo=codigo)
        
        # 2. Verificamos si existe el atributo 'usado'. 
        # Si no lo tienes en tu modelo, esto evitará el Error 500
        ya_fue_usado = getattr(boleto, 'usado', False)

        if ya_fue_usado:
            mensaje = "⚠️ ¡ESTE BOLETO YA FUE USADO!"
            clase_css = "error"
        else:
            # 3. Si tienes el campo 'usado', lo marcamos. Si no, solo mostramos éxito.
            if hasattr(boleto, 'usado'):
                boleto.usado = True
                boleto.save()
            
            mensaje = "✅ BOLETO VÁLIDO - BIENVENIDO"
            clase_css = "exito"

        return render(request, 'boletos/validar.html', {
            'boleto': boleto,
            'mensaje': mensaje,
            'clase_css': clase_css
        })

    except Exception as e:
        # Esto te mostrará el error real en la pantalla del celular si algo falla
        from django.http import HttpResponse
        return HttpResponse(f"Error en el servidor: {str(e)}", status=500)
    
def estadisticas(request):
    total = Boleto.objects.count()
    ingresados = Boleto.objects.filter(usado=True).count()
    faltantes = total - ingresados
    
    return render(request, 'boletos/stats.html', {
    'total': total,
    'ingresados': ingresados,
    'faltantes': faltantes,
    'porcentaje': (ingresados / total) * 100 if total > 0 else 0
    })