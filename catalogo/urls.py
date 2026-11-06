from django.urls import path
from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("catalogo/", views.lista_productos, name="lista"),
    path("catalogo/nuevo/", views.crear_producto, name="crear"),
    path("catalogo/<int:producto_id>/editar/", views.editar_producto, name="editar"),
    path("catalogo/<int:producto_id>/eliminar/", views.eliminar_producto, name="eliminar"),
    path("catalogo/<int:producto_id>/", views.detalle_producto, name="detalle"),
    path("login/", views.vista_login, name="login"),
    path("registro/", views.vista_registro, name="registro"),
    path("logout/", views.vista_logout, name="logout"),
    path("carrito/", views.ver_carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/actualizar/<int:producto_id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("carrito/vaciar/", views.vaciar_carrito, name="vaciar_carrito"),
    path("carrito/comprar/", views.realizar_compra, name="realizar_compra"),
    path("reportes/resumen/", views.reporte_resumen, name="reporte_resumen"),
    path("reportes/stock/", views.reporte_stock, name="reporte_stock"),
    path("consulta/", views.formulario_consulta, name="consulta"),
]
