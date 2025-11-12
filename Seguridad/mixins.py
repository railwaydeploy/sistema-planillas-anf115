from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth.views import redirect_to_login

class GroupPermissionRequiredMixin(LoginRequiredMixin, View):
    group_required = None  
    permissions_required = []  
    
    def dispatch(self, request, *args, **kwargs):
        if self.request is None:
            return HttpResponseBadRequest("La solicitud es inválida.")
        
        user = self.request.user

        # Verifica si el usuario está autenticado
        if not user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url=self.login_url)

        if self.group_required:
            # Verifica si el usuario pertenece al grupo
            if not user.groups.filter(name=self.group_required).exists():
                return self.handle_no_permission()

        # Verifica si el usuario tiene todos los permisos requeridos
        for permission in self.permissions_required:
            if not user.has_perm(permission):
                return HttpResponseForbidden("No tiene permisos suficientes para acceder a esta página.")
            
        return super().dispatch(request, *args, **kwargs)