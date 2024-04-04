from django.contrib import admin
from .models import product, category_front_page, brand, subcategory, category, rating, review
# Register your models here.
my_models = [product, category, category_front_page, brand, subcategory, rating, review]

admin.site.register(my_models)

admin.site.site_header = "SMART EXPRESS ADMIN"
admin.site.index_title = "SMART EXPRESS ADMIN"
admin.site.site_title = "SMART EXPRESS ADMIN"