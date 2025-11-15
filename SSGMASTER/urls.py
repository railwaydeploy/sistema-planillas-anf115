"""
URL configuration for SSGMASTER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import myadmin.urls
import empleado.urls
from django.http import JsonResponse
from django.urls import path

def devtools_json(_request):
    return JsonResponse({}, status=200)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include(myadmin.urls, namespace="myadmin")),
    path('', include('Seguridad.urls')),
    path('user/', include(empleado.urls, namespace="empleado")),
    path(".well-known/appspecific/com.chrome.devtools.json", devtools_json),
]
