from django.forms import ModelForm
from .models import product, brand, shop, category, category_front_page, subcategory

class addproduct(ModelForm):
    class Meta:
        fields = "__all__"
        model = product

class addbrand(ModelForm):
    class Meta:
        fields = "__all__"
        model = brand
    
class addshop(ModelForm):
    class Meta:
        fields = "__all__"
        model = shop

class addcategory(ModelForm):
    class Meta:
        fields = "__all__"
        model = category

class addcategory_front_page(ModelForm):
    class  Meta:
        fields = "__all__"
        model = category_front_page

class addsubcategory(ModelForm):
    class Meta:
        fields = "__all__"
        model = subcategory