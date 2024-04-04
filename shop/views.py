"""
Render function used to serve context to
Webpages.
"""
from django.shortcuts import render
#from .models import product, category, subcategory, rating, brand, category_front_page
# Create your views here.
def index(request):
    """
    View serving the home page logic
    """
    context = {
        "hello" : "Welcome to smart express",
        "title"  : "shop",
    }
    return render(request, 'index', context)

def product(request, category_slug, product_slug):
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
    context = {
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

def search(request, search_query):
    """
    To search products from the database
    """
    context = {
        'title' : 'search_results',
    }
    return render(request, 'search_results', context)