from django import forms

class RegistroForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre'}))
    apellidos = forms.CharField(label='Apellidos', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tus apellidos'}))
    curp = forms.CharField(label='CURP', max_length=18, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu CURP'}))
    correo = forms.EmailField(label='Correo', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo electrónico'}))
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'}))
    img = forms.ImageField(label='Imagen', required=False)