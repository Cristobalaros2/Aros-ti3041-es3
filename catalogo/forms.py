import re

from django import forms

from .models import Producto, ConsultaCliente

SOLO_LETRAS = re.compile(r"^[A-Za-záéíóúñüÁÉÍÓÚÑÜ.\s]+$")


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


class ConsultaClienteForm(forms.ModelForm):
    class Meta:
        model = ConsultaCliente
        fields = ["nombre", "correo", "producto", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Tu nombre y apellido"}),
            "correo": forms.EmailInput(attrs={"placeholder": "tu@gmail.com"}),
            "producto": forms.Select(attrs={"class": "select-consulta"}),
            "mensaje": forms.Textarea(attrs={"placeholder": "Escribe aquí tu consulta...", "rows": 5}),
        }
        labels = {
            "producto": "Producto de interés (opcional)",
        }
        help_texts = {
            "nombre": "Solo letras y espacios, sin números (mínimo 3 caracteres).",
            "correo": "Obligatorio: debe ser un correo @gmail.com.",
            "mensaje": "Entre 10 y 500 caracteres.",
        }

    def clean_nombre(self):
        nombre = " ".join((self.cleaned_data.get("nombre") or "").split())
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if any(caracter.isdigit() for caracter in nombre):
            raise forms.ValidationError("El nombre no puede contener números.")
        if not SOLO_LETRAS.fullmatch(nombre):
            raise forms.ValidationError("El nombre solo puede contener letras, espacios y puntos.")
        if not any(caracter.isalpha() for caracter in nombre):
            raise forms.ValidationError("El nombre debe contener letras.")
        return nombre

    def clean_correo(self):
        correo = (self.cleaned_data.get("correo") or "").strip().lower()
        if not correo:
            raise forms.ValidationError("El correo es obligatorio.")
        if " " in correo:
            raise forms.ValidationError("El correo no puede contener espacios.")
        if not correo.endswith("@gmail.com"):
            raise forms.ValidationError("El correo debe terminar en @gmail.com (ej: ana@gmail.com).")
        if correo.split("@")[0] == "":
            raise forms.ValidationError("El correo no es válido.")
        return correo

    def clean_mensaje(self):
        mensaje = (self.cleaned_data.get("mensaje") or "").strip()
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        if len(mensaje) > 500:
            raise forms.ValidationError("El mensaje no puede superar los 500 caracteres.")
        return mensaje
