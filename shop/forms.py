from django.forms import ModelForm
from .models import public_cart

class public_cart_form(ModelForm):
    class Meta:
        fields = ["first_name", "last_name", "phone_number", "region", "city", "address"]
        model = public_cart