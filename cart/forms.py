from django import forms

from mainapp.models import Product


class CartAddForm(forms.Form):
    # QUANTITY_CHOICES = [(i, str(i)) for i in range(1, )]

    quantity = forms.TypedChoiceField(choices=(), coerce=int)

    def __init__(self, *args, max_quantity=20, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].choices = [(i, str(i)) for i in range(1, max_quantity+1)]
