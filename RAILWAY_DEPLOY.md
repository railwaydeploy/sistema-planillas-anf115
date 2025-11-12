# Guía de Despliegue en Railway

Esta guía contiene los pasos exactos para desplegar este proyecto Django en Railway usando PostgreSQL, gunicorn y WhiteNoise.

## Prerequisitos

- Cuenta en Railway (https://railway.app)
- Repositorio en GitHub (o GitLab/Bitbucket) con este código
- Las dependencias y configuración ya están preparadas en el repo:
  - `Procfile` con gunicorn
  - `runtime.txt` con Python 3.11.9
  - `requirements.txt` con gunicorn, dj-database-url, psycopg2-binary, whitenoise
  - `SSGMASTER/settings.py` configurado para leer variables de entorno

## Pasos para Desplegar

### 1. Crear un nuevo proyecto en Railway

1. Ve a https://railway.app y haz login
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tu GitHub y selecciona el repositorio `sistema-planillas-anf115`
5. Railway detectará automáticamente que es un proyecto Python y usará `requirements.txt`

### 2. Añadir PostgreSQL

1. En el dashboard del proyecto Railway, click en "+ New"
2. Selecciona "Database" → "Add PostgreSQL"
3. Railway creará una base de datos PostgreSQL y añadirá automáticamente la variable de entorno `DATABASE_URL`

### 3. Configurar Variables de Entorno

1. En tu proyecto Railway, ve a la pestaña "Variables"
2. Añade las siguientes variables (click "+ New Variable"):

```
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-aqui
DEBUG=False
ALLOWED_HOSTS=tu-app.up.railway.app
```

**Importante:**
- Para `SECRET_KEY`: genera una clave segura (puedes usar https://djecrety.ir/ o ejecutar en Python: `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`)
- Para `ALLOWED_HOSTS`: Railway te dará una URL cuando despliegues (ej: `sistema-planillas-production.up.railway.app`). Usa esa URL aquí (sin http://).
- `DATABASE_URL` ya está configurada automáticamente por el plugin de PostgreSQL.

### 4. Desplegar

1. Railway desplegará automáticamente cuando hagas push al repo o cuando añades el proyecto
2. Espera a que el build termine (verás los logs en tiempo real)
3. Railway ejecutará:
   - `pip install -r requirements.txt`
   - Iniciará el servidor con el comando del `Procfile`: `gunicorn SSGMASTER.wsgi --bind 0.0.0.0:$PORT`

### 5. Ejecutar Migraciones y CollectStatic (IMPORTANTE)

Una vez desplegado, necesitas ejecutar las migraciones de base de datos y recoger archivos estáticos:

1. En Railway, ve a tu servicio/proyecto
2. Click en la pestaña "Settings"
3. Busca la sección "Service" y haz scroll hasta "Deploy"
4. Bajo "Custom Start Command", click en "Configure"
5. Puedes hacerlo de dos formas:

**Opción A: Desde Railway CLI (recomendado para primera vez)**

Instala Railway CLI:
```bash
npm i -g @railway/cli
# o
curl -fsSL https://railway.app/install.sh | sh
```

Luego ejecuta:
```bash
railway login
railway link  # selecciona tu proyecto
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser  # para crear usuario admin
```

**Opción B: Desde la consola web de Railway**

1. Ve a tu servicio en Railway
2. Click en "Settings" → "Service"
3. Haz scroll hasta la sección "Deploy"
4. Click en "Open Railway Shell" (si está disponible) o usa la sección "Deployments" → click en el deployment activo → "View Logs" y busca el botón de shell
5. Ejecuta:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Verificar el Despliegue

1. Railway te dará una URL pública (ej: `https://sistema-planillas-production.up.railway.app`)
2. Accede a esa URL en tu navegador
3. Prueba el login y el panel de admin en `/admin`

### 7. Actualizar `ALLOWED_HOSTS` (si es necesario)

Si no pusiste la URL correcta en `ALLOWED_HOSTS`:
1. En Railway → Variables
2. Edita `ALLOWED_HOSTS` y pon la URL exacta que te dio Railway (sin `https://`)
3. Railway redesplegará automáticamente

## Automatizar Migraciones (Opcional)

Si quieres que las migraciones y collectstatic se ejecuten automáticamente en cada deploy, puedes crear un script de release:

1. Crea un archivo `release.sh` en la raíz:
```bash
#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

2. Dale permisos de ejecución (localmente antes de hacer commit):
```bash
chmod +x release.sh
```

3. Modifica el `Procfile`:
```
release: ./release.sh
web: gunicorn SSGMASTER.wsgi --bind 0.0.0.0:$PORT
```

Railway ejecutará `release` antes de iniciar `web`.

## Problemas Comunes

### Error: "DisallowedHost"
- Solución: Verifica que `ALLOWED_HOSTS` en Railway contenga la URL exacta de tu app (sin `https://`)

### Error 500 o error al cargar archivos estáticos
- Solución: Ejecuta `python manage.py collectstatic --noinput` en Railway shell
- Verifica que `STATIC_ROOT` esté configurado en settings.py (ya está)

### Base de datos vacía / sin tablas
- Solución: Ejecuta `python manage.py migrate` en Railway shell

### Error al conectar a PostgreSQL
- Solución: Verifica que el plugin PostgreSQL esté activo y que `DATABASE_URL` esté en las variables de entorno

## Monitoreo y Logs

- Railway muestra logs en tiempo real en la pestaña "Deployments" → click en el deployment activo → "View Logs"
- Puedes ver métricas de CPU/RAM/Network en la pestaña "Metrics"

## Siguiente Paso: Configuración de Dominio Personalizado

Si quieres usar tu propio dominio:
1. En Railway → Settings → Domains
2. Click en "Add Domain"
3. Sigue las instrucciones para configurar DNS

---

**Resumen de Comandos Útiles (Railway CLI)**

```bash
# Login y conectar proyecto
railway login
railway link

# Ver logs en tiempo real
railway logs

# Ejecutar comandos en producción
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell

# Abrir el proyecto en el navegador
railway open
```

---

¡Listo! Tu aplicación Django debería estar corriendo en Railway con PostgreSQL, sirviendo archivos estáticos con WhiteNoise y lista para producción.
