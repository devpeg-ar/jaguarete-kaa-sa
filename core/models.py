from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class producto(models.Model):
    titulo = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="productos", null=True)
    descripcion = models.TextField()
    precio = models.IntegerField()
    categoria = models.ForeignKey(categoria, on_delete=models.PROTECT)
    destacado = models.BooleanField(default="False")

    def __str__(self):
        return self.titulo

class carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    productos = models.ManyToManyField(producto, blank=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Pedido Nro {self.id}"