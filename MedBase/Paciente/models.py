from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PacienteManager(BaseUserManager):
    def create_user(self, curp, email, password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(curp=curp, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, curp, email, password):
        user = self.create_user(curp, email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Paciente(AbstractBaseUser):
    curp = models.CharField(primary_key=True, max_length=10)
    email = models.EmailField('email address', unique=True)
    nombres = models.CharField("Nombre", max_length=35)
    apellidoPaterno = models.CharField("Apellido Paterno", max_length=25)
    apellidoMaterno = models.CharField("Apellido Materno", max_length=25)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PacienteManager()

    USERNAME_FIELD = 'curp'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'Paciente {self.curp}, {self.nombres}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# class  Consulta(models.Model):
#     paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
#     #medico = models.ForeignKey("Medico",on_delete=models.SET_NULL,null=True, blank=True)
#     enfermedad_actual = models.CharField(max_length=60)
#     antecedentes_personales = models.TextField()
#     antecedentes_familiares = models.TextField()
#     motivo_consulta = models.CharField(max_length=45)
#     diagnostico = models.CharField(max_length=70)
#     tratamiento = models.CharField(max_length=100)
#     fechahora_ingreso = models.DateTimeField(auto_now_add=True)

#     TENGO DUDAS SOBRE ESTÁ CLASE, NO ESTÓY SEGURO DE COMO LAS VAMOS A MANEJAR (Luisma)
