from datetime import datetime
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, View,DeleteView, UpdateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from myadmin.forms import *
from django.template.loader import get_template
from django.views import View
import xhtml2pdf.pisa as pisa
from django.contrib.auth.mixins import LoginRequiredMixin
from Seguridad.mixins import *
from django.contrib.auth.hashers import make_password

# Create your views here.
class MainTemplateView(GroupPermissionRequiredMixin,View):
    group_required = 'empleado'
    def get(self, request):
        # Lógica de la vista si es necesaria
        # Por ejemplo, puedes pasar datos a la plantilla
        context = {'dato': 'Hola desde la vista'}
        return render(request, 'baseuser.html', context)