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


class MainTemplateView(GroupPermissionRequiredMixin,View):
    group_required = 'Administrador'
    def get(self, request):
        # Lógica de la vista si es necesaria
        # Por ejemplo, puedes pasar datos a la plantilla
        context = {'dato': 'Hola desde la vista'}
        return render(request, 'baseview.html', context)


class DepartamentoView(GroupPermissionRequiredMixin,ListView):
    template_name='departamentoList.html'
    model=Departamento


class EmpleadoList(GroupPermissionRequiredMixin, ListView):
    template_name = 'empleadoList.html'
    model = Empleado
    group_required = 'Administrador'

class EmpleadoCreateView(GroupPermissionRequiredMixin, CreateView):
    model = Empleado
    template_name = 'createEmpleado.html'
    success_url = reverse_lazy('myadmin:EmpleadoList')
    group_required = 'Administrador'
    form_class = CreateEmpleadoForm

    def form_valid(self, form):
        user = Usuario.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
        empleado = form.save(commit=False)
        grupo_empleado, _ = Group.objects.get_or_create(name='empleado')

        empleado.fk_usuario = user
        user.groups.add(grupo_empleado)
        empleado.save()
        return super().form_valid(form)

class EmpleadoDeleteView(GroupPermissionRequiredMixin, DeleteView, SuccessMessageMixin):
    model=Empleado
    group_required = 'Administrador'
    success_url = reverse_lazy('myadmin:EmpleadoList')
    def get(self, request, *args, **kwargs):
        try:
            obj = Empleado.objects.get(id=self.kwargs[self.pk_url_kwarg])
            obj.delete()
            messages.success(request, "El receptor ha sido eliminado satisfactoriamente.")
            my_render = self.success_url
        except IntegrityError as e:
            messages.error(request, "La receptor no puede ser eliminado ya que tiene registros asociados")
            my_render = self.success_url
        return HttpResponseRedirect(my_render)

class EmpleadoUpdateView(GroupPermissionRequiredMixin, UpdateView, SuccessMessageMixin):
    model=Empleado
    group_required = 'Administrador'
    success_url = reverse_lazy('myadmin:EmpleadoList')
    template_name='updateEmpleado.html'
    form_class=UpdateEmpleadoForm

    def get_initial(self):
        initial = super().get_initial()
        if self.object.FK_municipio:
            departamento_id = self.object.FK_municipio.FK_departamento.SK_departamento if self.object.FK_municipio.FK_departamento else None
            print(departamento_id)

            if departamento_id:
                opciones_departamento = Departamento.objects.filter(SK_departamento=departamento_id).order_by("nombre")
                initial['Departamento'] = opciones_departamento.first()

            else:
                initial['Departamento'] = None
                initial['FK_municipio'] = []
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['query_municipio'] = Municipio.objects.order_by("nombre")

        return kwargs



class AdministradorList(GroupPermissionRequiredMixin,ListView):
    template_name ='administradorList.html'
    model = Usuario
    group_required = 'Administrador'

class AdministradorCreateView(GroupPermissionRequiredMixin,CreateView):
    model = Usuario
    template_name = "createAdministrador.html"
    success_url = reverse_lazy('myadmin:AdministradorList')
    group_required = 'Administrador'
    form_class = CreateAdministradorForm
    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])
        response = super().form_valid(form)
        grupo_administrador, _ = Group.objects.get_or_create(name='Administrador')
        self.object.groups.add(grupo_administrador)
        self.object.is_superuser = True
        self.object.is_staff = True
        self.object.save()
        return response

class AdministradorDeleteView(GroupPermissionRequiredMixin, DeleteView):
    model=Usuario
    group_required = 'Administrador'
    success_url = reverse_lazy('myadmin:AdministradorList')
    def get(self, request, *args, **kwargs):
        try:
            obj = Usuario.objects.get(SK_usuario=self.kwargs[self.pk_url_kwarg])
            grupo_administrador, _ = Group.objects.get_or_create(name='Administrador')
            grupo_administrador in obj.groups.all()
            obj.groups.remove(grupo_administrador)
            obj.delete()
            messages.success(request, "El administrador ha sido eliminado satisfactoriamente.")
            my_render = self.success_url
        except IntegrityError as e:
            messages.error(request, "El administrador no puede ser eliminado ya que tiene registros asociados")
            my_render = self.success_url
        return HttpResponseRedirect(my_render)


class AdministradorUpdateView(GroupPermissionRequiredMixin, UpdateView):
    model = Usuario
    template_name = "editAdministrador.html"
    success_url = reverse_lazy('myadmin:AdministradorList')
    group_required = 'Administrador'
    form_class = EditAdministradorForm

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo_administrador, _ = Group.objects.get_or_create(name='Administrador')
        self.object.groups.add(grupo_administrador)
        self.object.is_superuser = True
        self.object.is_staff = True
        self.object.save()
        return response


def load_muni(request):
    dep_id = request.GET.get('departamento')
    print("KLJASDJKLASD")
    munis = Municipio.objects.filter(FK_departamento=dep_id).order_by('nombre')
    return render(request, 'items_dropdown_list.html', {'items': munis})

def link_callback(uri, rel):

    if rel == 'stylesheet':
        return uri
    elif rel == 'icon':
        return uri
    else:
        return None

class empleadoPDFView(View):
    template_name = 'Reporte1.html'

    def get(self, request, *args, **kwargs):
        empleados = Empleado.objects.all()

        context = {
            'empleados': empleados,
        }

        # Encontrar la plantilla y renderizarla
        template = get_template(self.template_name)
        html = template.render(context)

        # Crear un PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_empleados.pdf"'  # Abre el PDF en línea

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)

        # Si hay errores, mostrar una vista de error
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

class listaEmpleadoPDFView(View):
    template_name = 'ReporteLista.html'

    def get(self, request, *args, **kwargs):
        empleados = Empleado.objects.all()

        context = {
            'empleados': empleados,
        }

        # Encontrar la plantilla y renderizarla
        template = get_template(self.template_name)
        html = template.render(context)

        # Crear un PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_empleados.pdf"'  # Abre el PDF en línea

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)

        # Si hay errores, mostrar una vista de error
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

class pdfTemplate(View):
    def get(self, request):
        # Lógica de la vista si es necesaria
        # Por ejemplo, puedes pasar datos a la plantilla
        context = {'dato': 'Hola desde la vista'}
        return render(request, 'Reporte1.html', context)

class PlantillaList(ListView, GroupPermissionRequiredMixin):
    template_name='PlanillaList.html'
    model=DetallePlanilla
    form_class=PlanillaSearchForm
    group_required="Administrador"

    def get(self, request):
        self.object_list = self.get_queryset()
        form = self.form_class()
        if form.is_valid():
            self.object_list = form.filter_queryset(request, self.object_list)
        context = self.get_context_data(object_list=self.object_list, form=form)
        return self.render_to_response(context)

class generetePlanillaEmpleado(FormView):
    template_name = 'PlanillaForm.html'
    form_class = createPlanillaEmpleado
    success_url=reverse_lazy("myadmin:PlanillaList")# Asegúrate de que el nombre del formulario sea correcto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Empleados"] = Empleado.objects.all()
        context["form"] = self.form_class()  # Asigna el formulario al contexto
        return context  # Debes devolver el contexto

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        detallPlan = DetallePlanilla()
        tramo1 = 472
        tramo2 = 895.24
        tramo3 = 2038.10
        empleado = Empleado.objects.get(id=self.request.POST.get('empleado',''))
        afp = (float(empleado.salario_base) *7.25)/100
        isss = float(empleado.salario_base) *0.03
        salario_bruto = float(empleado.salario_base) - isss - afp
        if salario_bruto <= tramo1:
            renta = 0
            salario_liquido = salario_bruto
        elif salario_bruto > tramo1 and salario_bruto <= tramo2:
            renta = ((salario_bruto - tramo1) * 0.10 + 17.67)
            salario_liquido = round(salario_bruto - renta, 2)
        elif salario_bruto > tramo2 and salario_bruto <= tramo3:
            renta = ((salario_bruto - tramo2) * 0.20 + 60.00)
            salario_liquido = round(salario_bruto - renta, 2)
        elif salario_bruto > tramo3:
            renta = ((salario_bruto - tramo3) * 0.30 + 288.57)
            salario_liquido = round(salario_bruto - renta, 2)
        detallPlan.Liquido_pagar = salario_liquido
        detallPlan.ISSS = isss
        detallPlan.RENTA= renta
        detallPlan.AFP = afp
        detallPlan.fecha_emision = datetime.strptime(self.request.POST.get('fecha',''), '%Y-%m-%d')
        detallPlan.FK_empleado= empleado
        detallPlan.dias_trabajados = self.request.POST.get('diasTrabajados','')
        detallPlan.horas_extras = self.request.POST.get('horasExtras','')
        detallPlan.save()

        return super().form_valid(form)

