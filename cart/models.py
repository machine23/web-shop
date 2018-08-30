from django.db import models
from mainapp.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart {} : {} {}'.format(self.user.username, self.product, self.quantity)
