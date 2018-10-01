from .models import Cart


def cart(request):
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).select_related()

    return {'cart': cart}
