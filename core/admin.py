from django.contrib import admin
from .models import categoria, producto, carrito


class ProductoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "precio", "categoria"]
    list_editable = ["precio", "categoria"]
    search_fields = ["titulo"]
    list_filter = ["precio", "categoria"]
    list_per_page = 5

# Register your models here.
admin.site.register(categoria)
admin.site.register(producto, ProductoAdmin)
admin.site.register(carrito)
