from django.contrib import admin
from pathlib import Path
from .models import product, category_front_page, brand, subcategory, category, rating, review
# Register your models here.
my_models = [product, category, category_front_page, brand, subcategory, rating, review]

BASE_DIR = Path(__file__).resolve().parent.parent
class MyModelAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tinymce/js/tinymce/custom.js',)


admin.site.register(my_models, MyModelAdmin)

admin.site.site_header = "SMART EXPRESS ADMIN"
admin.site.index_title = "SMART EXPRESS ADMIN"
admin.site.site_title = "SMART EXPRESS ADMIN"