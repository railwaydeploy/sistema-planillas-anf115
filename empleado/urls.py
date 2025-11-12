from django.urls import path
from .views import *

app_name = 'empleado' 
urlpatterns = [
    path('', MainTemplateView.as_view(), name="Home"),
]