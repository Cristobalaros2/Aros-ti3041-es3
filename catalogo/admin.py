from django.contrib import admin
from .models import Producto, ItemCarrito


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock")
    search_fields = ("nombre", "categoria")
    list_filter = ("categoria",)


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "producto", "cantidad")
    list_filter = ("usuario",)
    search_fields = ("usuario__username", "producto__nombre")
