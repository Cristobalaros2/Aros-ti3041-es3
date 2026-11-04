from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "categoria", "precio", "stock", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Martillo de uña"}),
            "categoria": forms.TextInput(attrs={"placeholder": "Ej: Herramientas manuales"}),
            "precio": forms.NumberInput(attrs={"min": 0, "placeholder": "Ej: 4990"}),
            "stock": forms.NumberInput(attrs={"min": 0, "placeholder": "Ej: 10"}),
            "imagen": forms.TextInput(attrs={"placeholder": "images/01-martillo.jpg"}),
        }
        labels = {
            "imagen": "Imagen (ruta estática)",
        }
        help_texts = {
            "imagen": "Ruta relativa dentro de static/, por ejemplo: images/01-martillo.jpg",
        }
