from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import producto, categoria, carrito
from .forms import ProductoForm, CustomUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from .search import search

# Create your views here.
def index(request):
    busqueda = request.GET.get("buscar")
    productos = producto.objects.all()
    categorias = categoria.objects.all()

    if busqueda:
        data = search(busqueda)
        return render(request, 'core/producto/listar.html', data)
    else:
        data = {
            'productos': productos,
            'categorias': categorias
        }
        return render(request, 'core/index.html', data)

def acerca_de(request):
    busqueda = request.GET.get("buscar")
    categorias = categoria.objects.all()
    if busqueda:
        data = search(busqueda)
        return render(request, 'core/producto/listar.html', data)
    else:
        data = {
            'categorias': categorias
        }
        return render(request, 'core/acerca_de.html', data)

@permission_required('core.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Producto agregado"
        else:
            data["form"] = formulario

    return render(request, 'core/producto/agregar.html', data)

@permission_required('core.change_producto')
def modificar_producto(request, id):

    prod = get_object_or_404(producto, id=id)

    data = {
        'form': ProductoForm(instance=prod)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=prod, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="inicio")
        else:
            data["form"] = formulario

    return render(request, 'core/producto/modificar.html', data)

def eliminar_producto(request, id):
    prod = get_object_or_404(producto, id=id)
    prod.delete()
    return redirect(to="inicio")

def ver_producto(request, id):
    busqueda = request.GET.get("buscar")
    categorias = categoria.objects.all()
    prod = get_object_or_404(producto, id=id)

    if busqueda:
        data = search(busqueda)
        return render(request, 'core/producto/listar.html', data)
    else:

        data = {
            'producto': prod,
            'categorias': categorias
        }

        return render(request, 'core/producto/producto.html', data)

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "El usuario ha sido creado correctamente")
            return redirect(to="inicio")
    return render(request, 'registration/registro.html', data)

def listar_productos(request, id):
    busqueda = request.GET.get("buscar")
    cat = get_object_or_404(categoria, id=id)
    categorias = categoria.objects.all()
    productos = producto.objects.all()
    
    if busqueda:
        data = search(busqueda)
    else:
        productos = producto.objects.filter(
            categoria = cat
        )
        data = {
            'cat': cat,
            'categorias': categorias,
            'productos': productos
        }
    return render(request, 'core/producto/listar.html', data)
@login_required
def carts(request):
    cart = carrito.objects.filter(usuario=request.user.id).first()
    categorias = categoria.objects.all()
    productos = producto.objects.all()

    if cart:
        prod_cart = cart.productos.all()       
        mensaje = ""
        data = {
            'cart': cart,
            'cart_prod': prod_cart,
            'productos': productos,
            'categorias': categorias,
            'mensaje': mensaje
        }
    else:
        mensaje = "No hay productos en el carrito"
        data = {
            'cart': cart,
            'mensaje': mensaje,
            'productos': productos,
            'categorias': categorias
        }
    
    return render(request, 'core/carrito.html', data)

def update_cart(request, id):
    user_cart = carrito.objects.filter(usuario=request.user.id).first()
    productos = producto.objects.get(id=id)

    if user_cart:
        if not productos in user_cart.productos.all():
            user_cart.productos.add(productos)
        else:
            user_cart.productos.remove(productos)

        new_total = 0

        for item in user_cart.productos.all():
            new_total += item.precio

        user_cart.total = new_total
        user_cart.save()
    else:
        new_cart = carrito()
        new_cart.usuario = request.user
        new_cart.save()
        

        if not productos in new_cart.productos.all():
            new_cart.productos.add(productos)
        else:
            new_cart.productos.remove(productos)

        new_total = 0

        for item in new_cart.productos.all():
            new_total += item.precio

        new_cart.total = new_total
        new_cart.save()
    
    return HttpResponseRedirect(reverse("carrito"))

def clear_cart(request):
    cart = carrito.objects.filter(usuario=request.user.id).first()

    for p in cart.productos.all():
        cart.productos.remove(p)

    cart.total = 0
    cart.save()

    return redirect(to="carrito")