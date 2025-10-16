from django import forms

# Formulario para TEMAS
class TemaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label='Tema',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Ahorro Personal'})
    )
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={
            'placeholder': 'Ahorrar es guardar una parte de tu dinero para gastarlo después, en lugar de gastarlo todo de una vez. Es como guardar una semilla para que crezca más tarde y puedas comprar algo que te gusta mucho, como un juguete o una bicicleta. ',
            'rows': 4
        })
    )
