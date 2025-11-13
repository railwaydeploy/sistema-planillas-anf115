#!/bin/bash

echo "🚀 Ejecutando script de release para Railway..."

echo "📦 Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Script de release completado exitosamente!"
