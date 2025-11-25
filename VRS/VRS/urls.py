from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from SystemCore.views import index as Dashboard, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Página principal de la app
    path('home/', Dashboard, name='index'),
    # Autenticación (login/logout)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Use custom logout view that accepts GET and POST to avoid 405 errors
    path('accounts/logout/', logout_view, name='logout'),
    # Redirigir la raíz del sitio a la página 'home'
    path('', RedirectView.as_view(pattern_name='index', permanent=False), name='root-redirect'),
]