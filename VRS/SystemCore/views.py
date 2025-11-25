from django.shortcuts import render
from .models import *

from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculos, Registro, RegistroVehiculo

def index(request):
    # --- CUANDO SE ENVÍA UN FORMULARIO ---
    if request.method == "POST":

        # Crear o actualizar Vehiculo
        if "save_vehiculo" in request.POST:
            id = request.POST.get("vehiculo_id")
            if id:  # update
                v = Vehiculos.objects.get(id=id)
                v.patente = request.POST["patente"]
                v.marca = request.POST["marca"]
                v.modelo = request.POST["modelo"]
                v.vigente = "vigente" in request.POST
                v.save()
            else:  # create
                Vehiculos.objects.create(
                    patente=request.POST["patente"],
                    marca=request.POST["marca"],
                    modelo=request.POST["modelo"],
                )
            return redirect("index")

        # Eliminar Vehiculo
        if "delete_vehiculo" in request.POST:
            Vehiculos.objects.get(id=request.POST["vehiculo_id"]).delete()
            return redirect("index")

        # Crear o actualizar Registro
        if "save_registro" in request.POST:
            id = request.POST.get("registro_id")
            if id:
                r = Registro.objects.get(id=id)
                r.tipo_registro = request.POST["tipo"]
                r.descripcion = request.POST["descripcion"]
                r.vigente = "vigente" in request.POST
                r.save()
            else:
                Registro.objects.create(
                    tipo_registro=request.POST["tipo"],
                    descripcion=request.POST["descripcion"],
                )
            return redirect("index")

        # Eliminar Registro
        if "delete_registro" in request.POST:
            Registro.objects.get(id=request.POST["registro_id"]).delete()
            return redirect("index")

        # Crear / actualizar RegistroVehiculo
        if "save_rv" in request.POST:
            id = request.POST.get("rv_id")
            fecha_salida = request.POST.get("fecha_salida") or None

            if id:
                rv = RegistroVehiculo.objects.get(id=id)
                rv.vehiculo_id = request.POST["vehiculo"]
                rv.registros_id = request.POST["registro"]
                rv.fecha_salida = fecha_salida
                rv.save()
            else:
                RegistroVehiculo.objects.create(
                    vehiculos_id=request.POST["vehiculo"],
                    registro_id=request.POST["registro"],
                )
            return redirect("index")

        # Eliminar RegistroVehiculo
        if "delete_rv" in request.POST:
            RegistroVehiculo.objects.get(id=request.POST["rv_id"]).delete()
            return redirect("index")

    # --- CARGAR DATOS PARA MOSTRAR ---
    contexto = {
        "vehiculos": Vehiculos.objects.all(),
        "registros": Registro.objects.all(),
        "rv_list": RegistroVehiculo.objects.all(),
    }

    return render(request, "index.html", contexto)