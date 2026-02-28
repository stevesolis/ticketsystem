from django.contrib import admin
from .models import Evento, Boleto

admin.site.register(Evento)

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    # Columnas que verás en la lista principal
    list_display = ('nombre_asistente', 'codigo', 'evento', 'usado')
    
    # Filtros laterales (Muy útil para ver quién falta por entrar)
    list_filter = ('usado', 'evento')
    
    # Buscador por nombre o código UID
    search_fields = ('nombre_asistente', 'codigo')
    
    # Permite marcar boletos como usados o no usados masivamente
    actions = ['marcar_como_no_usado']

    def marcar_como_no_usado(self, request, queryset):
        queryset.update(usado=False)
    marcar_como_no_usado.short_description = "Resetear boletos seleccionados (Marcar como NO usado)"