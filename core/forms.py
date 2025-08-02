from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Pasajero, Reserva

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre', 'documento', 'email', 'telefono', 'fecha_nacimiento', 'tipo_documento']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vuelo', 'pasajero', 'asiento', 'precio', 'estado']

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    documento = forms.CharField(max_length=30)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tipo_documento = forms.CharField(max_length=50)

    class Meta:
        model = Usuario
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'cliente'
        if commit:
            user.save()
            Pasajero.objects.create(
                usuario=user,
                nombre=self.cleaned_data['nombre'],
                documento=self.cleaned_data['documento'],
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data['telefono'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                tipo_documento=self.cleaned_data['tipo_documento'],
            )
        return user
