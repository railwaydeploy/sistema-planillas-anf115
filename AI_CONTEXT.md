AI_CONTEXT.md
===============

Propósito
--------
Este archivo ofrece un resumen conciso y operativo del proyecto "sistema-planillas-anf115" para que un asistente (IA) comprenda la arquitectura, cómo levantar el proyecto y dónde encontrar las piezas clave del código.

Visión general del proyecto
---------------------------
- Tipo: Aplicación web Django (backend + templates HTML, sin SPA).  
- Versión objetivo de Python: 3.11.x (en este repositorio se usó 3.11.9).  
- Framework: Django 4.2.x.  
- Base de datos esperada: MySQL (el proyecto incluye `mysqlclient` en `requirements.txt`), aunque puede funcionar con SQLite si configuras `DATABASES` en `SSGMASTER/settings.py`.

Estructura relevante (principal)
--------------------------------
- `manage.py` — Entrypoint de Django.
- `SSGMASTER/` — configuración del proyecto (contains `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
- Apps:
  - `myadmin/` — contiene muchas vistas, plantillas y migraciones (modelos principales relacionados con planillas, empleados, etc.).
  - `empleado/` — app relacionada con empleados.
  - `Seguridad/` — login, forms, mixins y vistas de seguridad/autenticación.
- `static/` — assets CSS/JS/imagenes usados por las vistas.
- `templates/` dentro de cada app (y `myadmin/templates`) — plantillas HTML.

Archivos clave a revisar primero
--------------------------------
- `SSGMASTER/settings.py` — configuración (apps instaladas, middlewares, rutas estáticas, DB, locales).  
- `myadmin/models.py` — modelos del dominio (planilla, empleado, detalle, etc.).  
- `myadmin/views.py`, `myadmin/urls.py` — rutas y controladores.  
- `Seguridad/views.py` y `Seguridad/forms.py` — manejo de login/registro/permiso.  
- `templates/` y `myadmin/templates/` — layout y páginas principales (dashboard, PlanillaList, Reportes).

Cómo levantar el proyecto (resumen reproducible)
------------------------------------------------
Requisitos previos: Python 3.11.x instalado (ej. 3.11.9), acceso a Internet para instalar dependencias, y un servidor de base de datos si no usas SQLite.

1) Crear y activar virtualenv (usa el Python que prefieras):

Bash (Windows con Git Bash / WSL):

```bash
python -m pip install --user virtualenv        # si necesitas virtualenv
python -m virtualenv .venv || python -m venv .venv
# Activar (bash)
source .venv/Scripts/activate
```

PowerShell (Windows):

```powershell
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias:

```bash
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

3) Configurar base de datos (si usas MySQL): ajustar `SSGMASTER/settings.py` -> `DATABASES` con credenciales y host.

4) Migraciones y superusuario:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5) Ejecutar servidor de desarrollo:

```bash
python manage.py runserver 0.0.0.0:8000
# o solo: python manage.py runserver
```

6) Accede en el navegador: http://127.0.0.1:8000 (o la IP del host si usas contenedores).

Notas y problemas frecuentes detectados
--------------------------------------
- Algunas instalaciones de Python (p.ej. Laragon) pueden tener `python311._pth` con `import site` comentado, lo que hace que `pip` no sea importable de forma directa. Si ocurre esto, instalar pip con `get-pip.py` y/o ejecutar `pip` forzando `site-packages` en `sys.path` es una solución. En la sesión actual se creó `.venv` usando el Python de Laragon con un workaround.
- Dependencias nativas: `mysqlclient` y `lxml` requieren ruedas precompiladas en Windows o las herramientas de compilación apropiadas (MSVC). Si fallan, instala las ruedas para tu versión de Python o instala las dependencias del sistema.
- Los archivos estáticos se encuentran en `static/`. En desarrollo Django sirve esos archivos automáticamente con `runserver` cuando `DEBUG=True`.

Puntos de interés del dominio
-----------------------------
- La app `myadmin` implementa gran parte de la lógica de planillas (migraciones numeradas 0001..0006 indican modelos y cambios); revisar `myadmin/models.py` y `myadmin/views.py` para comprender la entidad "Planilla" y su relación con `Empleado`.
- `empleado` contiene lógica específica del empleado; `Seguridad` maneja la autenticación y permisos.
- Existe uso de librerías para manejar PDF/Reportes: `xhtml2pdf`, `pyHanko`, `reportlab`, `pypdf`. Eso significa que el proyecto genera reportes y firmados digitales.

Comandos útiles para desarrolladores y para la IA
-------------------------------------------------
- Ejecutar pruebas:
  - `python manage.py test` (Ejecuta tests de apps si existen).  
- Revisar migraciones: `python manage.py makemigrations --dry-run --verbosity 3`  
- Inspeccionar URLs: `python manage.py show_urls` (requiere django-extensions) o revisar `SSGMASTER/urls.py` y los `urls.py` de cada app.
- Ejecutar shell de Django: `python manage.py shell` para inspeccionar modelos desde Python.

Contrato para la IA (cómo puedo ayudar eficazmente)
---------------------------------------------------
- Entrada: fragmentos de código, rutas, vistas o descripción de la tarea que quieras implementar (feature, bugfix, tests, refactor).  
- Salida esperada: cambios en archivos del repo (edits pequeños y explicables), instrucciones reproducibles para ejecutar, y pruebas unitarias mínimas cuando aplique.  
- Reglas: no modificar archivos sin revisión; cuando haga cambios, los enumeraré y correré migraciones/tests locales si proceden.

Siguientes recomendaciones para mejorar la on-boarding de la IA
----------------------------------------------------------------
- Añadir un `CONTRIBUTING.md` o `DEV_SETUP.md` con la configuración de base de datos local (ej. docker-compose para MySQL) y variables de entorno.  
- Añadir un script `bin/setup` o `Makefile` que cree el `.venv` y ejecute `pip install -r requirements.txt` y `manage.py migrate` automáticamente.  
- Añadir `django-extensions` y el comando `show_urls` al `requirements.txt` para facilitar exploración.

Contacto
--------
Si necesitas que amplíe este archivo con un mapa detallado de modelos (campos principales por modelo), o con un diagrama de rutas y autorización, dímelo y lo genero escaneando `myadmin/models.py`, `empleado/models.py` y `Seguridad/models.py`.

----
Archivo generado automáticamente por el asistente de desarrollo. Mantener en la raíz para referencia rápida.
