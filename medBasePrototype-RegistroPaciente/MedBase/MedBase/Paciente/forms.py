from django import forms
from .models import Paciente

class RegistroForm(forms.ModelForm):
    #encriptar el password
    password = forms.CharField(widget=forms.PasswordInput)

    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.SelectDateWidget(years=range(1900, 2100)),
        required=False
    )

    class Meta:
        model = Paciente
        #Campos del model que se van a tomar
        fields = ['username', 'email', 'nombres', 'apellido_paterno', 'apellido_materno', 'genero', 'nombre_calle', 'numero_calle', 'municipio', 'estado', 'fecha_nacimiento', 'password']

    #Ejemplo de metodo por si se necesitan los elementos por separado
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

