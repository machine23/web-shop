from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views import View

from cart.forms import CartAddForm

from .models import Category, Product


def index(request):
    featured = Product.objects.all()[:4]
    trending = Product.objects.all()[:3]

    context = {
        'featured': featured,
        'trending': trending,
    }
    return render(request, 'mainapp/index.html', context)


def details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = product.category.products.exclude(pk=pk)
    cart_form = CartAddForm(max_quantity=product.stock)

    context = {
        'product': product,
        'related': related,
        'cart_form': cart_form
    }
    return render(request, 'mainapp/details.html', context)


def products(request, category_pk=None):
    categories = Category.objects.all()
    products = Product.objects.all()

    category = None
    if category_pk:
        category = get_object_or_404(Category, pk=category_pk)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'mainapp/products.html', context)


def contacts(request):
    return render(request, 'mainapp/contacts.html')


class ProductAPIView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.GET.get('id'))
        return JsonResponse(model_to_dict(product, exclude=['image']))
