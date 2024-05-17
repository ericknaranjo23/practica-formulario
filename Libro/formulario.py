from django import forms

class GeneroForms(forms.Form):
    nombre_genero = forms.CharField(max_length=50, label='Genero')

class AutorForms(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    apellido = forms.CharField(max_length=100, label='Apellido')
    fecha_nacimiento = forms.DateTimeField(label='Fecha de Nacimiento', required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))