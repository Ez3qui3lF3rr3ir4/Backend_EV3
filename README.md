# VRS - Instrucciones de instalación y puesta en marcha (Windows / PowerShell)

Este README explica, paso a paso, cómo clonar el repositorio, crear un entorno virtual, configurar variables de entorno y ejecutar el proyecto Django en un entorno de desarrollo Windows (PowerShell).

Requisitos previos
- Python 3.11+ instalado (en este proyecto se desarrolló con Python 3.13.7).
- Git instalado.
- MySQL disponible si quieres usar la configuración por defecto que está en `VRS/settings.py` (opcional: puedes usar SQLite para desarrollo local, ver sección correspondiente).

Resumen rápido (comandos rápidos)
```powershell
# Clonar (reemplaza la URL por la del repositorio correcto)
git clone https://github.com/<usuario>/<repo>.git
cd <repo>\VRS

# Crear y activar entorno virtual (Windows PowerShell)
python -m venv .venv
# Si PowerShell no permite activar, ejecutar (permite solo en la sesión actual):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
. .venv\Scripts\Activate.ps1

# Instalar dependencias (si existe requirements.txt) o paquetes básicos
pip install -r requirements.txt  # si existe
# si NO existe, instalar al menos Django y python-dotenv
pip install "django==5.2.8" python-dotenv

# Crear archivo .env con variables necesarias (ver sección .env más abajo)

# Ejecutar migraciones y crear superusuario
python manage.py migrate
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

Pasos detallados

1) Clonar el repositorio

- Abre PowerShell y clona el repo:

```powershell
git clone https://github.com/<usuario>/<repo>.git
cd <repo>\VRS
```

Reemplaza la URL por la del repositorio real si corresponde.

2) Crear y activar entorno virtual (PowerShell)

```powershell
python -m venv .venv
# En PowerShell, activa con:
. .venv\Scripts\Activate.ps1
```

Nota sobre políticas de ejecución de PowerShell: si recibes un error al activar el entorno, permite scripts solo para la sesión actual:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
. .venv\Scripts\Activate.ps1
```

3) Instalar dependencias

- Si el repo dispone de `requirements.txt`:

```powershell
pip install -r requirements.txt
```

- Si no existe `requirements.txt`, instala al menos los paquetes principales usados por el proyecto:

```powershell
pip install "django==5.2.8" python-dotenv
# Si vas a usar MySQL (configuración por defecto):
pip install mysqlclient
# Alternativa si tienes problemas con mysqlclient en Windows:
pip install PyMySQL
# y agrega (opcional) la compatibilidad en el proyecto: en `VRS/__init__.py` añadir:
"""
# Si usas PyMySQL en Windows, puedes forzar que actúe como MySQLdb:
import pymysql
pymysql.install_as_MySQLdb()
"""
```

4) Configurar variables de entorno (.env)

El proyecto usa `python-dotenv` y lee variables en `VRS/settings.py`. Crea un archivo `.env` en la raíz `VRS/` (misma carpeta que `manage.py`) con el contenido mínimo:

```text
# .env (ejemplo)
SECRET_KEY=tu_secreto_aqui
DEBUG=True
DATABASE=nombre_bd
USER=usuario_mysql
PASSWORD_DB=tu_password
HOST=127.0.0.1
PORT=3306
```

Importante: no subas `.env` al repositorio. Añádelo a `.gitignore` si aún no está.

5) Opciones: usar SQLite en desarrollo local (más simple)

Si no quieres configurar MySQL localmente, puedes usar SQLite para desarrollo. Abre `VRS/settings.py` y reemplaza la sección `DATABASES` por:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Luego no necesitas variables de entorno para la BD.

6) Migraciones y usuario administrador

```powershell
python manage.py migrate
python manage.py createsuperuser
```

7) Ejecutar servidor de desarrollo

```powershell
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en tu navegador. Para acceder al admin: `http://127.0.0.1:8000/admin/`.

8) Archivos estáticos (solo en despliegue o cuando configures collectstatic)

Para desarrollo local Django sirve archivos estáticos automáticamente cuando `DEBUG=True`. Si preparas despliegue, ejecuta:

```powershell
python manage.py collectstatic
```

y configura `STATIC_ROOT` en `VRS/settings.py` apropiadamente.

9) Variables de settings que revisar

- `SECRET_KEY`: en desarrollo puedes poner un valor corto, en producción no.
- `DEBUG`: en producción debe ser `False`.
- `ALLOWED_HOSTS`: añadir hosts cuando `DEBUG=False`.

10) Solución de problemas comunes

- Error al instalar `mysqlclient` en Windows: usar ruedas (wheels) o instalar Visual C++ Build Tools, o usar `PyMySQL` como alternativa.
- `ModuleNotFoundError: dotenv`: instala `python-dotenv` (`pip install python-dotenv`).
- `TemplateSyntaxError` por filtros de fecha: revisa comillas en templates (ej: `{{ fecha|date:"Y-m-d\\TH:i" }}`).

11) Notas sobre git remoto y push

- Si al hacer `git push` recibes `remote: Repository not found`, verifica que la URL del remoto es correcta y que tienes permisos en GitHub. Configura remoto así (reemplaza por tu repo):

```powershell
git remote add origin https://github.com/<tu-usuario>/<tu-repo>.git
git push -u origin main
```

12) Desarrollo adicional

- El proyecto ya incluye la app `SystemCore` con templates y archivos estáticos en `SystemCore/static/SystemCore/`.
- Recomendación: crea `requirements.txt` con tus dependencias una vez que las instales:

```powershell
pip freeze > requirements.txt
```

Contribuciones y contacto
- Si quieres que te ayude a crear un `requirements.txt` preciso o a dockerizar la base MySQL para desarrollo, dímelo y lo agrego.

---

Archivo creado automáticamente por el asistente — si quieres que incluya instrucciones específicas (por ejemplo, detalles para instalar `mysqlclient` en Windows o configurar Docker Compose para MySQL), dime y lo añado.
