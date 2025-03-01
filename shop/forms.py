from django.forms import ModelForm
from .models import public_cart, public_reviews
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class public_cart_form(ModelForm):
    class Meta:
        fields = ["first_name", "last_name", "phone_number", "region", "city", "address"]
        model = public_cart

class public_review_form(ModelForm):
    class Meta:
        model = public_reviews
        fields = ["customer_fullname", "customer_rating", "customer_feedback"]

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
