from django import forms


class ShippingAddressForm(forms.Form):
    """Formulario para recoger la dirección de envío de productos físicos."""
    
    nombre_completo = forms.CharField(
        max_length=150,
        label="Nombre completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre completo'
        })
    )
    direccion = forms.CharField(
        max_length=255,
        label="Dirección",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle, número, piso...'
        })
    )
    ciudad = forms.CharField(
        max_length=100,
        label="Ciudad",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad'
        })
    )
    codigo_postal = forms.CharField(
        max_length=20,
        label="Código postal",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código postal'
        })
    )
    provincia = forms.CharField(
        max_length=100,
        label="Provincia / Estado",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Provincia'
        })
    )
    pais = forms.CharField(
        max_length=100,
        label="País",
        initial="España",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'País'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        label="Teléfono (opcional)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono de contacto'
        })
    )
    
    def get_formatted_address(self):
        """Retorna la dirección formateada como texto"""
        parts = [
            self.cleaned_data.get('nombre_completo'),
            self.cleaned_data.get('direccion'),
            f"{self.cleaned_data.get('codigo_postal')} {self.cleaned_data.get('ciudad')}",
            self.cleaned_data.get('provincia'),
            self.cleaned_data.get('pais'),
        ]
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            parts.append(f"Tel: {telefono}")
        return ", ".join(filter(None, parts))
