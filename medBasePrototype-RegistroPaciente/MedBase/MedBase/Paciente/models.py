from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PacienteManager(BaseUserManager):
    def create_user(self, username, email, password=None, nombres='', apellido_paterno='', apellido_materno='', genero='', nombre_calle='', numero_calle='', municipio='', estado='', fecha_nacimiento=None):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, nombres=nombres, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, genero=genero, nombre_calle=nombre_calle, numero_calle=numero_calle, municipio=municipio, estado=estado, fecha_nacimiento=fecha_nacimiento)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, nombres='', apellido_paterno='', apellido_materno='', genero='', nombre_calle='', numero_calle='', municipio='', estado='', fecha_nacimiento=None):
        user = self.create_user(username, email, password=password, nombres=nombres, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, genero=genero, nombre_calle=nombre_calle, numero_calle=numero_calle, municipio=municipio, estado=estado, fecha_nacimiento=fecha_nacimiento)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Paciente(AbstractBaseUser):
    username = models.CharField('CURP', unique=True, max_length=18)
    email = models.EmailField('Correo', unique=True)
    nombres = models.CharField("Nombre(s)", max_length=35, blank=True, default='')
    apellido_paterno = models.CharField("Apellido Paterno", max_length=25, blank=True, default='')
    apellido_materno = models.CharField("Apellido Materno", max_length=25, blank=True, default='')
    genero = models.CharField("Género", max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True, default='')
    nombre_calle = models.CharField("Nombre de calle", max_length=100, blank=True, default='')
    numero_calle = models.CharField("Número de calle", max_length=10, blank=True, default='')
    municipio = models.CharField("Municipio", max_length=100, blank=True, default='')
    estado = models.CharField("Estado", max_length=100, blank=True, default='')
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PacienteManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username','email','password']

    def __str__(self):
        return f'Paciente {self.username}, {self.nombres} {self.apellido_paterno} {self.apellido_materno}'

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