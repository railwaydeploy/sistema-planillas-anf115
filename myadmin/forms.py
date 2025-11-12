from datetime import datetime
from django import forms
from .models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm

class CreateEmpleadoForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        required=False,
        queryset=Departamento.objects.order_by("nombre"),
        label="Departamento"
    )
    username = forms.CharField(max_length=150, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)

    
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellidos', 'documento', 'direccion', 'telefono', 'cargo', 'departamento', 'FK_municipio','salario_base','username', 'password1', 'password2', 'email']
        widgets = {
            'documento': forms.TextInput(attrs={'placeholder': '________-_', 'data-mask': '9999999-9', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['FK_municipio'].queryset = Municipio.objects.none()
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['FK_municipio'].queryset = Municipio.objects.filter(
                    FK_departamento=departamento_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Talla queryset
        elif self.instance.pk:
            self.fields['FK_municipio'].queryset = self.instance.Departamento.FK_municipio_set.order_by(
                'descripcion')
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        # Verificar si el nombre de usuario ya existe
        if username:
            existing_user = Usuario.objects.filter(username=username).first()
            if existing_user:
                self.add_error('username', "Este nombre de usuario ya está en uso. Por favor, elija otro nombre de usuario.")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden. Por favor, inténtelo de nuevo.")

        return cleaned_data
    
class UpdateEmpleadoForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(required=False,
        queryset=Departamento.objects.order_by("nombre"), label="Departamento")

    class Meta:
        model = Empleado
        fields = ['nombre', 'apellidos', 'documento', 'direccion', 'telefono', 'cargo', 'departamento', 'FK_municipio']
        widgets = {
            'documento': forms.TextInput(attrs={'placeholder': '________-_', 'data-mask': '9999999-9', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        query_municipio = kwargs.pop('query_municipio')

        super().__init__(*args, **kwargs)
        self.fields['FK_municipio'].queryset = query_municipio
            
class CreateAdministradorForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                'placeholder': "Ingrese de nuevo la contraseña",
            }),
        label='Confirmación contraseña',
        required=True
    )


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.")

    class Meta:
        model = Usuario
        fields = ['password','username','first_name','last_name','password', 'password_confirm', 'email','fecha_contratacion']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese el nombre",
                    'required': 'required'
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese el apellido",
                    'required': 'required'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese el nombre de usuario",
                    'required': 'required'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese la contraseña",
                    'required': 'required'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese la dirección de correo electrónico",
                    'required': 'required'
                }
            ),
            'fecha_contratacion':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/aaaa'}),
        }


class EditAdministradorForm(forms.ModelForm):

    class Meta:
        model = Usuario
        exclude =  ['password']
        fields = ['username','first_name','last_name','password', 'email','fecha_contratacion']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese el nombre",
                    'required': 'required'
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese el apellido",
                    'required': 'required'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese el nombre de usuario",
                    'required': 'required'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ingrese la dirección de correo electrónico",
                    'required': 'required'
                }
            ),
            'fecha_contratacion':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/aaaa'}),
        }
        
class createPlanillaEmpleado(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'autocomplete':"off"}))
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all())
    diasTrabajados = forms.IntegerField(max_value=31)
    horasExtra = forms.IntegerField()
    diasVacaciones = forms.IntegerField()
    
class PlanillaSearchForm(forms.Form):
   fecha_ini = forms.CharField(required=False)
   fecha_fin = forms.CharField(required=False)
   def filter_queryset(self, request, queryset):
        fechaini_selected = self.cleaned_data['fecha_ini']
        qs = queryset
        if fechaini_selected:
            fecha_ini = self.cleaned_data['fecha_ini']
            fecha_fin = self.cleaned_data['fecha_fin']
            if fecha_ini:
                aware_ini = (datetime.strptime(fecha_ini, '%Y-%m-%d'))
            else:
                aware_ini = None

            if fecha_fin:
                aware_fin = (datetime.strptime(fecha_fin, '%Y-%m-%d'))
            else:
                aware_fin = None
            qs = qs.filter(fecha__range = (aware_ini,aware_fin))
        return qs
    