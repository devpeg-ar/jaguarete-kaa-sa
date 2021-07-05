from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="inicio"),
    path('acerca_de/', views.acerca_de, name="acerca_de"),
    path('agregar-producto/', views.agregar_producto, name="agregar_producto"),
    path('modificar-producto/<id>/', views.modificar_producto, name="modificar_producto"),
    path('eliminar-producto/<id>/', views.eliminar_producto, name="eliminar_producto"),
    path('producto/<id>/', views.ver_producto, name="ver_producto"),
    path('registro/', views.registro, name="registro"),
    path('listar_productos/<id>/', views.listar_productos, name="listar-productos"),
    path('carrito/', views.carts, name="carrito"),
    path('carrito/<id>/', views.update_cart, name="actualizar_carrito"),
    path('vaciar-carrito/', views.clear_cart, name="limpiar_carrito"),
]