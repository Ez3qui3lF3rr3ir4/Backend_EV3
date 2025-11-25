from django.db import models

class Vehiculos(models.Model):
    patente = models.CharField(max_length=10, unique=True, null=False)
    modelo = models.CharField(max_length=50, null=False)
    marca = models.CharField(max_length=50, null=False)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.patente}"

class Registro(models.Model):
    tipo_registro = models.CharField(max_length=50, null=False)
    descripcion = models.TextField(null=True, blank=True)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo_registro}"

class RegistroVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Registro de {self.vehiculo} - {self.registro} - Ingreso: {self.fecha_ingreso} - Egreso {self.fecha_salida}"
    