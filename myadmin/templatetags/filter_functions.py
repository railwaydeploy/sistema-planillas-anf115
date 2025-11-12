from django import template

import datetime
from django.utils.safestring import mark_safe
from django.conf import settings

from myadmin.models import Municipio
register = template.Library()

@register.simple_tag
def muestra_municipios(id_master):
    qs = Municipio.objects.filter(FK_departamento=id_master).order_by("nombre")
    devolver = ""
    fila = 1
    for entry in qs:
        devolver =devolver+ "<tr>" \
                  "<td>"+str(fila)  +"</td>" \
                  "<td>" + entry.nombre + "</td></tr>"
        fila+=1
    return mark_safe(devolver)