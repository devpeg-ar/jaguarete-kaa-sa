from .models import producto, categoria
from django.db.models import Q

def search(busqueda):
    categorias = categoria.objects.all()
    productos = producto.objects.filter(
        Q(titulo__icontains = busqueda) |
        Q(descripcion__icontains = busqueda)
    ).distinct()

    data = {
        'productos': productos,
        'categorias': categorias
    }

    return data