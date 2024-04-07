"""
Render function used to serve context to
Webpages.
"""
from django.shortcuts import render, redirect
from .forms import addbrand, addcategory, addcategory_front_page, addproduct, addshop, addsubcategory
from .models import product, category, subcategory, rating, brand, category_front_page
# Create your views here.
def index(request):
    """
    View serving the home page logic
    """
    c = category.objects.all()
    categories = [c[:4], c[4:]]
    s = subcategory.objects.all()[:4]
    p = product.objects.all()[5:9]
    context = {
        "products": p,
        "subs" : s,
        "categories": categories,
        "hello" : "Welcome to smart express",
        "title"  : "shop",
    }
    return render(request, 'index', context)

def single_product(request, category_slug, product_slug):
    """
    This displays details of a product in a particular category
    """
    context = {
        "hello" : "Welcome to smart express",
        "title"  : "product_title",
    }
    return render(request, 'product', context)

def products(request, category_slug):
    """
    This displays products in a particular category
    """
    categories = subcategory.objects.all()
    context = {
        "categories" : categories,
        "hello" : "Welcome to smart express",
        "title"  : "category_title",
    }
    return render(request, 'products', context)

def subproducts(request, category_slug, subcategory_slug, product_slug):
    """
    This displays products in a subcategory
    """
    context = {
        "title" : "product_detail",
    }
    return render(request, 'product', context=context)

def search(request):
    """
    To search products from the database
    """
    if request.POST:
        search_query = request.POST['search_query']
    search_package = product.objects.filter(name__icontains=str(search_query))
    context = {
        'title' : str(search_query),
        'products' : search_package,
    }
    return render(request, 'search_results', context)