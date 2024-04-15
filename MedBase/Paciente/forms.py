from django import forms
from .models import Paciente

class RegistroForm(forms.ModelForm):
    #encriptar el password
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Paciente
        #Campos del model que se van a tomar
        fields = ['curp', 'email', 'nombres', 'apellidoPaterno', 'apellidoMaterno', 'password']

    #Ejemplo de metodo por si se necesitan los elementos por separado
    def clean_curp(self):
        curp = self.cleaned_data.get('curp')
        return curp
