from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Paciente(AbstractBaseUser):
    curp = models.CharField(primary_key=True,max_length=10)
    #password = models.CharField('',max_length=100)
    email = models.EmailField(('email address'), blank=False, null=False, unique=True)
    imgen =  models.ImageField('Imagen de Perfil',upload_to='perfil/', height_field=None)
    nombres = models.CharField("Nombre", max_length=35)
    apellidoPaterno = models.CharField("Apellido Paterno", max_length=25)
    apellidoMaterno = models.CharField("Apellido Materno", max_length=25)
    
    USERNAME_FIELD =  'curp'
    REQUIRED_FIELDS = ['curp','password', 'email', 'nombre']
    
    def  __str__(self):
        return f'Paciente {self.curp},{self.nombres}'
    
    def  has_perm(self, perm, obj=None):
        return True
    
    def  has_module_perms(self, module):
        return True
    
    @property
    def  is_staff(self):
        return self.usuario_administrador


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