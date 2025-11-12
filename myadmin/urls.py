from django.urls import path
from .views import *
from . import views

app_name = 'myadmin' 
urlpatterns = [
    path('', MainTemplateView.as_view(), name="inicio"),
    path('departamentoList',DepartamentoView.as_view(), name="DepartamentoList"),
    path('empleadoList',EmpleadoList.as_view(), name="EmpleadoList"),
    path('empleadoAdd',EmpleadoCreateView.as_view(),name="EmpleadoAdd"),
    path('empleadoDelete/<int:pk>',EmpleadoDeleteView.as_view(), name="EmpleadoDelete"),
    path('empleaedoUpdate/<int:pk>',EmpleadoUpdateView.as_view(), name="EmpleadoUpdate"),
    path('administradorList', AdministradorList.as_view(), name="AdministradorList"),
    path('administradorAdd', AdministradorCreateView.as_view(), name="AdministradorAdd"),
    path('administradorEdit/<int:pk>/', AdministradorUpdateView.as_view(), name='AdministradorEdit'),
    path('administradorDelete/<int:pk>/', AdministradorDeleteView.as_view(), name="AdministradorDelete"),
    path('loadMunis',views.load_muni, name='ajax_load_munis'),
    path('generate-pdf/', empleadoPDFView.as_view(), name='generate_pdf'),
    path('generar-pdf-empleados/', listaEmpleadoPDFView.as_view(), name='generar_pdf_empleados'),
    path('testTemplate/',pdfTemplate.as_view(),name='template_pdf'),
    path('PlanillaList/',PlantillaList.as_view(), name='PlanillaList'),
    path('genPlanillaForm/',generetePlanillaEmpleado.as_view(), name='PlanillaForm')

]