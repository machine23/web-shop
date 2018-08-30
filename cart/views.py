from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from mainapp.models import Product
from .models import Cart


@login_required
def cart_add(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.filter(user=user, product=product)

    if cart:
        cart[0].quantity += 1
        cart[0].save()
    else:
        Cart.objects.create(user=user, product=product, quantity=1)

    return redirect(product.get_absolute_url())


def cart_remove(request, product_id):

    return redirect('shop:index')
