from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from SystemCore.views import index as Dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    # Página principal de la app
    path('home/', Dashboard, name='index'),
    # Redirigir la raíz del sitio a la página 'home'
    path('', RedirectView.as_view(pattern_name='index', permanent=False), name='root-redirect'),
]
