from django.shortcuts import render
from .models import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Vehiculos, Registro, RegistroVehiculo
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods


def _format_exception(e):
    """Return a user-friendly string for ValidationError/IntegrityError or generic exceptions."""
    try:
        # Django ValidationError can have message_dict or messages
        if hasattr(e, 'message_dict') and e.message_dict:
            parts = []
            for field, msgs in e.message_dict.items():
                if isinstance(msgs, (list, tuple)):
                    parts.append(f"{field}: {', '.join(msgs)}")
                else:
                    parts.append(f"{field}: {msgs}")
            return '; '.join(parts)
        if hasattr(e, 'messages') and e.messages:
            return '; '.join(str(m) for m in e.messages)
    except Exception:
        pass
    # IntegrityError or other exceptions
    try:
        return str(e)
    except Exception:
        return 'Error desconocido.'

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
                try:
                    v.full_clean()
                    v.save()
                    messages.success(request, "Vehículo actualizado correctamente.")
                except (ValidationError, IntegrityError) as e:
                    messages.error(request, f"Error al actualizar vehículo: {_format_exception(e)}")
            else:  # create
                try:
                    v = Vehiculos(
                        patente=request.POST["patente"],
                        marca=request.POST["marca"],
                        modelo=request.POST["modelo"],
                    )
                    v.full_clean()
                    v.save()
                    messages.success(request, "Vehículo creado correctamente.")
                except IntegrityError:
                    messages.error(request, f"La patente {request.POST.get('patente')} ya existe.")
                except ValidationError as e:
                    messages.error(request, f"Datos inválidos para vehículo: {_format_exception(e)}")
            return redirect("index")

        # Eliminar Vehiculo
        if "delete_vehiculo" in request.POST:
            try:
                Vehiculos.objects.get(id=request.POST["vehiculo_id"]).delete()
                messages.success(request, "Vehículo eliminado.")
            except Exception as e:
                messages.error(request, f"Error al eliminar vehículo: {_format_exception(e)}")
            return redirect("index")

        # Crear o actualizar Registro
        if "save_registro" in request.POST:
            id = request.POST.get("registro_id")
            if id:
                r = Registro.objects.get(id=id)
                r.tipo_registro = request.POST["tipo"]
                r.descripcion = request.POST["descripcion"]
                r.vigente = "vigente" in request.POST
                try:
                    r.full_clean()
                    r.save()
                    messages.success(request, "Registro actualizado correctamente.")
                except (ValidationError, IntegrityError) as e:
                    messages.error(request, f"Error al actualizar registro: {_format_exception(e)}")
            else:
                try:
                    r = Registro(
                        tipo_registro=request.POST["tipo"],
                        descripcion=request.POST["descripcion"],
                    )
                    r.full_clean()
                    r.save()
                    messages.success(request, "Registro creado correctamente.")
                except ValidationError as e:
                    messages.error(request, f"Datos inválidos para registro: {_format_exception(e)}")
                except IntegrityError as e:
                    messages.error(request, f"Error al crear registro: {_format_exception(e)}")
            return redirect("index")

        # Eliminar Registro
        if "delete_registro" in request.POST:
            try:
                Registro.objects.get(id=request.POST["registro_id"]).delete()
                messages.success(request, "Registro eliminado.")
            except Exception as e:
                messages.error(request, f"Error al eliminar registro: {_format_exception(e)}")
            return redirect("index")

        # Crear / actualizar RegistroVehiculo
        if "save_rv" in request.POST:
            id = request.POST.get("rv_id")
            fecha_salida = request.POST.get("fecha_salida") or None

            if id:
                rv = RegistroVehiculo.objects.get(id=id)
                rv.vehiculo_id = request.POST["vehiculo"]
                rv.registro_id = request.POST["registro"]
                rv.fecha_salida = fecha_salida
                try:
                    rv.full_clean()
                    rv.save()
                    messages.success(request, "Registro vehículo actualizado.")
                except (ValidationError, IntegrityError) as e:
                    messages.error(request, f"Error al actualizar registro vehículo: {_format_exception(e)}")
            else:
                try:
                    rv = RegistroVehiculo(
                        vehiculo_id=request.POST["vehiculo"],
                        registro_id=request.POST["registro"],
                    )
                    rv.full_clean()
                    rv.save()
                    messages.success(request, "Registro de vehículo creado.")
                except ValidationError as e:
                    messages.error(request, f"Datos inválidos para registro vehículo: {_format_exception(e)}")
                except IntegrityError as e:
                    messages.error(request, f"Error al crear registro vehículo: {_format_exception(e)}")
            return redirect("index")

        # Eliminar RegistroVehiculo
        if "delete_rv" in request.POST:
            try:
                RegistroVehiculo.objects.get(id=request.POST["rv_id"]).delete()
                messages.success(request, "Registro de vehículo eliminado.")
            except Exception as e:
                messages.error(request, f"Error al eliminar registro vehículo: {_format_exception(e)}")
            return redirect("index")

    # --- CARGAR DATOS PARA MOSTRAR ---
    contexto = {
        "vehiculos": Vehiculos.objects.all(),
        "registros": Registro.objects.all(),
        "rv_list": RegistroVehiculo.objects.all(),
    }

    return render(request, "index.html", contexto)


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Log out the user (accept GET or POST) and redirect to index with a message."""
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('index')