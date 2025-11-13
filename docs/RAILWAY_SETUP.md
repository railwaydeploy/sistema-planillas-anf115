# Railway Setup - Configuración Técnica del Proyecto

Este documento explica la configuración técnica del proyecto Django para su despliegue en Railway.

## 📋 Descripción General

Este proyecto Django ha sido configurado para desplegarse en Railway usando:
- **Base de datos**: PostgreSQL (proveída por Railway)
- **Servidor web**: Gunicorn
- **Archivos estáticos**: WhiteNoise
- **Runtime**: Python 3.11.9

## 🛠️ Archivos de Configuración

### 1. `Procfile`
Define los procesos que Railway ejecutará:

```
release: bash scripts/release.sh
web: gunicorn SSGMASTER.wsgi --bind 0.0.0.0:$PORT
```

- **release**: Se ejecuta antes del despliegue (migraciones y collectstatic)
- **web**: Inicia el servidor Gunicorn en el puerto asignado por Railway

### 2. `runtime.txt`
Especifica la versión de Python:

```
python-3.11.9
```

### 3. `requirements.txt`
Contiene todas las dependencias necesarias:

**Dependencias de Django:**
- `Django==4.2.3`
- `django-phonenumber-field==7.2.0`
- `django-widget-tweaks==1.5.0`
- `xhtml2pdf==0.2.11`

**Dependencias para Railway/Producción:**
- `gunicorn==20.1.0` - Servidor WSGI para producción
- `dj-database-url==1.2.0` - Parser para DATABASE_URL
- `psycopg2-binary==2.9.9` - Adaptador PostgreSQL
- `whitenoise==6.5.0` - Servidor de archivos estáticos
- `python-dotenv==1.0.0` - Manejo de variables de entorno

### 4. `scripts/release.sh`
Script automatizado que se ejecuta antes de cada despliegue:

```bash
#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

Ejecuta automáticamente las migraciones y recolecta archivos estáticos.

## ⚙️ Configuración en `settings.py`

### Variables de Entorno

El proyecto lee las siguientes variables de entorno:

| Variable | Descripción | Valor por Defecto | Requerido en Prod |
|----------|-------------|-------------------|-------------------|
| `SECRET_KEY` | Clave secreta de Django | Valor de desarrollo | ✅ Sí |
| `DEBUG` | Modo debug | `True` | ✅ Sí (debe ser `False`) |
| `ALLOWED_HOSTS` | Hosts permitidos | `.127.0.0.1,.localhost` | ✅ Sí |
| `DATABASE_URL` | URL de conexión PostgreSQL | SQLite local | ✅ Sí (auto en Railway) |

### Configuración de Base de Datos

```python
# Por defecto usa SQLite (desarrollo local)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Si DATABASE_URL existe (Railway), usa PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
```

### Configuración de Archivos Estáticos

```python
# Archivos estáticos (desarrollo)
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

# Carpeta donde collectstatic reúne todos los archivos (producción)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise para servir archivos estáticos comprimidos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Middleware de WhiteNoise

WhiteNoise está configurado en el middleware para servir archivos estáticos eficientemente:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Debe estar después de SecurityMiddleware
    # ... resto del middleware
]
```

### Seguridad para HTTPS

```python
# Honra el header X-Forwarded-Proto para HTTPS (necesario en Railway)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

## 🔄 Flujo de Despliegue en Railway

1. **Push a GitHub** → Railway detecta cambios
2. **Build**:
   - Railway instala Python 3.11.9
   - Ejecuta `pip install -r requirements.txt`
3. **Release** (proceso `release` del Procfile):
   - Ejecuta `scripts/release.sh`
   - Aplica migraciones: `python manage.py migrate --noinput`
   - Recolecta estáticos: `python manage.py collectstatic --noinput`
4. **Deploy** (proceso `web` del Procfile):
   - Inicia Gunicorn: `gunicorn SSGMASTER.wsgi --bind 0.0.0.0:$PORT`
5. **Listo** → Aplicación disponible en la URL de Railway

## 📦 Variables de Entorno en Railway

Debes configurar estas variables en Railway Dashboard → Variables:

```env
SECRET_KEY=<tu-clave-secreta-generada>
DEBUG=False
ALLOWED_HOSTS=<tu-app>.up.railway.app
```

**Nota**: `DATABASE_URL` se configura automáticamente cuando añades PostgreSQL.

## 🔐 Generar SECRET_KEY

Opción 1 - Usar djecrety.ir:
- Visita: https://djecrety.ir/
- Copia la clave generada

Opción 2 - Desde Python:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🗃️ Estructura de Base de Datos

El proyecto usa el modelo de usuario personalizado:
```python
AUTH_USER_MODEL = 'myadmin.Usuario'
```

**Apps con modelos**:
- `myadmin` - Gestión de usuarios, empleados, planillas
- `Seguridad` - Autenticación y permisos
- `empleado` - Portal del empleado

## 📊 Migraciones

Las migraciones existentes incluyen:
- Creación de modelos iniciales
- Campos adicionales (municipio código, salario base, etc.)
- Relaciones entre empleados y planillas

Al ejecutar `migrate` en Railway, todas estas migraciones se aplicarán a PostgreSQL.

## 🌐 URLs y Routing

- `/` - Login
- `/admin/` - Panel de administración Django
- `/main/` - Dashboard principal
- Otras rutas definidas en apps `myadmin`, `empleado`, `Seguridad`

## 📝 Archivos Ignorados (.gitignore)

```gitignore
venv/
db.sqlite3        # No subir la BD local
.vscode*/
*.log
*.pyc
__pycache__/
media/
```

El archivo `db.sqlite3` no se sube a GitHub (Railway usará PostgreSQL).

## 🚨 Solución de Problemas Comunes

### Error: DisallowedHost at /
**Causa**: `ALLOWED_HOSTS` no incluye el dominio de Railway

**Solución**:
1. Ve a Railway → Variables
2. Edita `ALLOWED_HOSTS` con tu URL exacta (ej: `mi-app.up.railway.app`)
3. Railway redesplegará automáticamente

### Error 500 - Server Error
**Causa**: Posibles problemas con archivos estáticos o migraciones

**Solución**:
1. Verifica logs en Railway: Deployments → View Logs
2. Asegúrate que el script `release.sh` se ejecutó correctamente
3. Verifica que `DEBUG=False` en variables de entorno

### Static files no se cargan
**Causa**: `collectstatic` no se ejecutó

**Solución**:
- El script `release.sh` lo ejecuta automáticamente
- Si falla, ejecuta manualmente: `railway run python manage.py collectstatic --noinput`

### Base de datos vacía
**Causa**: Migraciones no aplicadas

**Solución**:
- El script `release.sh` lo ejecuta automáticamente
- Crea superusuario: `railway run python manage.py createsuperuser`

## 📚 Recursos Adicionales

- [Documentación de Railway](https://docs.railway.app/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## ✅ Checklist Pre-Despliegue

Antes de desplegar, verifica:

- [ ] Código subido a GitHub
- [ ] `requirements.txt` actualizado con todas las dependencias
- [ ] `Procfile` con comandos release y web
- [ ] `runtime.txt` con versión de Python
- [ ] `scripts/release.sh` con permisos de ejecución (ejecutable)
- [ ] `.gitignore` incluye `db.sqlite3`, `venv/`, etc.
- [ ] `settings.py` configurado para leer variables de entorno
- [ ] WhiteNoise en middleware
- [ ] PostgreSQL añadido en Railway
- [ ] Variables de entorno configuradas (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- [ ] Superusuario creado después del primer deploy

---

**Última actualización**: 12 de noviembre de 2025
