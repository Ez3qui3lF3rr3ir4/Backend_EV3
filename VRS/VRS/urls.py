from django.contrib import admin
from django.urls import path
from SystemCore.views import index as Dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', Dashboard, name='index'),
]
