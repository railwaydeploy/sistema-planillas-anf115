DEV_SETUP.md
=============

Este archivo contiene los pasos para levantar el proyecto en un entorno local Windows (también válidos en bash/WSL con pequeñas diferencias).

1) Crear y activar entorno virtual (Windows - PowerShell o CMD)

PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD (o Git Bash / WSL -> usar source en su lugar):
```cmd
python -m venv .venv
.venv\Scripts\activate
```

Bash (Git Bash / WSL):
```bash
python -m venv .venv
source .venv/Scripts/activate
```

2) Instalar dependencias

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

3) Configurar base de datos local (opcional - usar SQLite) — fragmento para `SSGMASTER/settings.py`:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

(Nota: si ya tienes otra configuración en `settings.py` no es estrictamente necesario cambiarla; usa la que prefieras.)

4) Aplicar migraciones

```bash
python manage.py migrate
```

5) (Opcional) Crear superusuario

```bash
python manage.py createsuperuser
```

5.b) Opcional: asignar un usuario al grupo "Administrador" desde el shell de Django

```bash
python manage.py shell

from django.contrib.auth.models import Group
from myadmin.models import Usuario

grupo, _ = Group.objects.get_or_create(name='Administrador')
usuario = Usuario.objects.get(username='admin')  # usa el nombre que creaste
usuario.groups.add(grupo)
usuario.save()
exit()
```

6) Lanzar servidor de desarrollo en el puerto 8001

```bash
python manage.py runserver 8001
```

Notas y recomendaciones
- Si usas Windows y PowerShell y recibes un error de ejecución al activar `.venv\Scripts\Activate.ps1`, ejecuta en PowerShell (con permisos de admin si es necesario):
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
- Si utilizas Laragon o un Python con `python311._pth` y ves que pip no está disponible, usa `get-pip.py` para instalar pip en esa instalación, o crea y usa `.venv` con `virtualenv` como hicimos en la sesión.
- Para servir estáticos en producción usa WhiteNoise o configura un storage externo (S3).

Si quieres, puedo:
- Crear un archivo `start_dev.bat` para Windows que haga la activación del venv y arranque el servidor en 8001.
- Aplicar el cambio en `SSGMASTER/settings.py` para forzar SQLite local si me lo autoriza.  
- Ejecutar los comandos aquí para ti (crear superusuario, arrancar servidor, etc.).
