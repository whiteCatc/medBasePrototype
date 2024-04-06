from django.contrib.auth.backends import ModelBackend
from .models import Paciente

class PacienteBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            paciente = Paciente.objects.get(username=username)
            if paciente.check_password(password):
                return paciente
        except Paciente.DoesNotExist:
            return None
