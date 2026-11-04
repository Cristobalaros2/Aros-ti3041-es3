from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.views.decorators.http import require_POST

from .forms import ProductoForm
from .models import Producto, ItemCarrito


def staff_required(view):
    """Solo administradores del sitio pueden gestionar el catálogo desde la web."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Inicia sesión con una cuenta de administrador para gestionar el catálogo.")
            return redirect("catalogo:login")
        if not request.user.is_staff:
            messages.error(request, "No tienes permisos para gestionar el catálogo.")
            return redirect("catalogo:lista")
        return view(request, *args, **kwargs)

    return wrapper


def _contexto_base(request):
    user = request.user
    autenticado = user.is_authenticated
    return {
        "username": user.username if autenticado else None,
        "es_admin": autenticado and user.is_staff,
        "cart_count": ItemCarrito.objects.filter(usuario=user).count() if autenticado else 0,
    }


# === VISTAS PÚBLICAS ===

def landing_page(request):
    destacados = Producto.objects.order_by("-precio")[:4]
    return render(request, "catalogo/landing.html", {
        **_contexto_base(request),
        "destacados": destacados,
    })


def lista_productos(request):
    productos = Producto.objects.all()
    total = productos.count()
    disponibles = productos.filter(stock__gt=0).count()
    agotados = total - disponibles
    return render(request, "catalogo/lista.html", {
        **_contexto_base(request),
        "productos": productos,
        "total": total,
        "disponibles": disponibles,
        "agotados": agotados,
    })


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "catalogo/detalle.html", {
        **_contexto_base(request),
        "producto": producto,
    })


# === CRUD DEL CATÁLOGO (SOLO ADMIN) ===

@staff_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f"Producto '{producto.nombre}' creado correctamente.")
            return redirect("catalogo:lista")
        messages.error(request, "No se pudo crear el producto. Revisa los campos marcados.")
    else:
        form = ProductoForm()

    return render(request, "catalogo/producto_form.html", {
        **_contexto_base(request),
        "form": form,
        "titulo": "Nuevo producto",
        "boton": "Crear producto",
    })


@staff_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Producto '{producto.nombre}' actualizado correctamente.")
            return redirect("catalogo:lista")
        messages.error(request, "No se pudo actualizar el producto. Revisa los campos marcados.")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "catalogo/producto_form.html", {
        **_contexto_base(request),
        "form": form,
        "titulo": f"Editar: {producto.nombre}",
        "boton": "Guardar cambios",
        "producto": producto,
    })


@staff_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre}' eliminado del catálogo.")
        return redirect("catalogo:lista")

    return render(request, "catalogo/confirmar_eliminar.html", {
        **_contexto_base(request),
        "producto": producto,
    })


# === AUTH ===

def vista_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {username}!")
            return redirect("catalogo:lista")
        messages.error(request, "Usuario o contraseña incorrectos.")
        return render(request, "catalogo/login.html", {"error": True})
    return render(request, "catalogo/login.html")


def vista_registro(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        errores = []
        if not username:
            errores.append("El usuario es obligatorio.")
        elif len(username) < 3:
            errores.append("El usuario debe tener al menos 3 caracteres.")
        elif username == "admin":
            errores.append("Ese nombre de usuario no está disponible.")
        elif User.objects.filter(username=username).exists():
            errores.append("Ese usuario ya existe.")
        if password1 != password2:
            errores.append("Las contraseñas no coinciden.")
        elif len(password1) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")

        if errores:
            return render(request, "catalogo/registro.html", {"errores": errores, "username": username, "email": email})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, "Cuenta creada exitosamente.")
        return redirect("catalogo:lista")

    return render(request, "catalogo/registro.html")


def vista_logout(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("catalogo:lista")


# === CARRITO ===

@require_POST
def agregar_al_carrito(request, producto_id):
    if not request.user.is_authenticated:
        messages.error(request, "Inicia sesión para agregar al carrito.")
        return redirect("catalogo:login")

    producto = get_object_or_404(Producto, id=producto_id)
    item, creado = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    if not creado:
        item.cantidad += 1
        item.save()
    messages.success(request, f"'{producto.nombre}' agregado al carrito.")
    return redirect("catalogo:lista")


def ver_carrito(request):
    if not request.user.is_authenticated:
        messages.error(request, "Inicia sesión para ver tu carrito.")
        return redirect("catalogo:login")

    items = ItemCarrito.objects.filter(usuario=request.user).select_related("producto")
    carrito = [
        {
            "id": item.producto.id,
            "nombre": item.producto.nombre,
            "precio": item.producto.precio,
            "imagen": item.producto.imagen,
            "cantidad": item.cantidad,
        }
        for item in items
    ]
    total = sum(i["precio"] * i["cantidad"] for i in carrito)
    return render(request, "catalogo/carrito.html", {
        **_contexto_base(request),
        "carrito": carrito,
        "total": total,
    })


@require_POST
def actualizar_carrito(request, producto_id):
    if not request.user.is_authenticated:
        return redirect("catalogo:login")

    accion = request.POST.get("accion")
    item = ItemCarrito.objects.filter(usuario=request.user, producto_id=producto_id).first()
    if item is None:
        return redirect("catalogo:carrito")

    if accion == "sumar":
        item.cantidad += 1
        item.save()
    elif accion == "restar":
        item.cantidad -= 1
        if item.cantidad <= 0:
            item.delete()
        else:
            item.save()
    elif accion == "eliminar":
        item.delete()
    return redirect("catalogo:carrito")


@require_POST
def vaciar_carrito(request):
    if not request.user.is_authenticated:
        return redirect("catalogo:login")
    ItemCarrito.objects.filter(usuario=request.user).delete()
    messages.info(request, "Carrito vaciado.")
    return redirect("catalogo:carrito")


@require_POST
def realizar_compra(request):
    if not request.user.is_authenticated:
        messages.error(request, "Inicia sesión para comprar.")
        return redirect("catalogo:login")

    items = ItemCarrito.objects.filter(usuario=request.user).select_related("producto")
    if not items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect("catalogo:carrito")

    sin_stock = [i.producto.nombre for i in items if i.producto.stock < i.cantidad]
    if sin_stock:
        messages.error(
            request,
            f"Stock insuficiente para: {', '.join(sin_stock)}. Reduce la cantidad o elimina estos productos.",
        )
        return redirect("catalogo:carrito")

    total = 0
    items_comprados = []
    with transaction.atomic():
        for item in items:
            item.producto.stock -= item.cantidad
            item.producto.save()
            subtotal = item.producto.precio * item.cantidad
            total += subtotal
            items_comprados.append({
                "id": item.producto.id,
                "nombre": item.producto.nombre,
                "precio": item.producto.precio,
                "imagen": item.producto.imagen,
                "cantidad": item.cantidad,
                "subtotal": subtotal,
            })
        items.delete()

    messages.success(request, "¡Compra realizada exitosamente!")
    return render(request, "catalogo/compra_exitosa.html", {
        **_contexto_base(request),
        "items": items_comprados,
        "total": total,
        "cart_count": 0,
    })
