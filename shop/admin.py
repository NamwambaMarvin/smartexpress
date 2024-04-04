from django.contrib import admin
from .models import product, category_front_page, brand, subcategory, category, rating, review
# Register your models here.
my_models = [product, category, category_front_page, brand, subcategory, rating, review]

admin.site.register(my_models)