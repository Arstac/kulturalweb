# booking/forms.py
from django import forms

class ContactoArtistaForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Tu nombre')
    email = forms.EmailField(label='Tu email')
    mensaje = forms.CharField(widget=forms.Textarea, label='Mensaje')