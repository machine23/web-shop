from django.contrib.auth.models import User
from django.db import models

from mainapp.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart {} : {} ({})'.format(self.user.username, self.product, self.quantity)

    def get_total_quantity(self):
        items = Cart.objects.filter(user=self.user)
        return sum(i.quantity for i in items) or 0
