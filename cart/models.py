from django.contrib.auth.models import User
from django.db import models

from mainapp.models import Product


class CartQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        print('***** Cart.objects.delete')
        for object in self:
            object.product.stock += object.quantity
            object.product.save()
        super().delete(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return 'Cart {} : {} ({})'.format(self.user.username, self.product, self.quantity)

    def get_total_quantity(self):
        items = Cart.objects.filter(user=self.user)
        return sum(i.quantity for i in items)

    def get_total_price(self):
        items = Cart.objects.filter(user=self.user)
        return sum(i.quantity * i.product.price for i in items)

    def delete(self):
        print('***** Cart.delete')
        self.product.stock += self.quantity
        self.product.save()
        super().delete()

    def save(self, *args, **kwargs):
        if self.pk:
            old_quantity = Cart.objects.get(pk=self.pk).quantity
            self.product.stock -= self.quantity - old_quantity
        else:
            self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
