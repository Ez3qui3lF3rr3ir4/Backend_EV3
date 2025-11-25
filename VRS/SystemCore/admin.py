from django.contrib import admin
from .models import Vehiculos, Registro, RegistroVehiculo

class VehiculosAdmin(admin.ModelAdmin):
    list_display = ('patente', 'modelo', 'marca', 'vigente')
    search_fields = ('patente', 'modelo', 'marca')
    list_filter = ('vigente',)

admin.site.register(Vehiculos, VehiculosAdmin)

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('tipo_registro', 'vigente')
    search_fields = ('tipo_registro',)
    list_filter = ('vigente',)

admin.site.register(Registro, RegistroAdmin)

class RegistroVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'registro', 'fecha_ingreso', 'fecha_salida')
    search_fields = ('vehiculo__patente', 'registro__tipo_registro')
    list_filter = ('fecha_ingreso', 'fecha_salida')

admin.site.register(RegistroVehiculo, RegistroVehiculoAdmin)