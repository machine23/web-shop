from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict

from mainapp.models import Product

from .forms import CartAddForm
from .models import Cart


@login_required
def cart_details(request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        item.form = CartAddForm(initial={'quantity': item.quantity})
    context = {
        'cart': cart,
    }
    return render(request, 'cart/details.html', context)


@require_POST
@login_required
def cart_add(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.filter(user=user, product=product)

    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart_item = None
        if cart:
            cart_item = cart[0]
            cart_item.quantity += cd['quantity']
            cart_item.save()
        else:
            cart_item = Cart.objects.create(user=user, product=product, quantity=cd['quantity'])

        result = {
            'status': 'ok',
            'cart_quantity': cart_item.get_total_quantity(),
            'cart_price': cart_item.get_total_price(),
        }
    else:
        result = {
            'status': 'error',
        }

    return JsonResponse(result)

@require_POST
@login_required
def cart_update_quantity(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    cart_item = Cart.objects.get(user=user, product=product)

    form = CartAddForm(request.POST)
    if form.is_valid() and cart_item:
        cart_item.quantity = form.cleaned_data['quantity']
        cart_item.save()

        result = {
            'status': 'updated',
            'product': model_to_dict(product, exclude=['image',]),
            'quantity': cart_item.quantity,
            'total_quantity': cart_item.get_total_quantity(),
            'total_price': cart_item.get_total_price(),
        }
    else:
        result = {
            'status': 'error',
        }
    
    return JsonResponse(result)




def cart_remove(request, product_id):
    cart_item = get_object_or_404(Cart, pk=product_id)
    cart_item.delete()

    return redirect('cart:cart_details')
