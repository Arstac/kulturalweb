from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)  # Llama al método save del formulario base, pero no guarda el usuario en la base de datos aún.
        user.email = self.cleaned_data['email']  # Establece el email del usuario con el valor proporcionado en el formulario.
        if commit:
            user.save()  # Guarda el usuario en la base de datos.
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)