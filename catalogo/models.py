from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField(default=0)
    imagen = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class ItemCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="carrito_items")
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("usuario", "producto")

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} x{self.cantidad}"
