"""
Render function used to serve context to
Webpages.
"""
from django.shortcuts import render, redirect
from .forms import addbrand, addcategory, addcategory_front_page, addproduct, addshop, addsubcategory
from .models import product, category, subcategory, rating, brand, category_front_page
from django.db.models import Q
# Create your views here.
def index(request):
    """
    View serving the home page logic
    """
    c = category.objects.all()
    categories = [c[:4], c[4:]]
    s = subcategory.objects.all()[:4]
    p = product.objects.order_by('?')[5:9]
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
    c = category.objects.get(slug=category_slug)
    p = product.objects.get(slug=product_slug, category=c)
    context = {
        "title"  : p.name,
        "product" : p,
    }
    return render(request, 'product', context)

def products(request, category_slug):
    """
    This displays products in a particular category
    """
    # Try to fetch products in
    # either a category or sub category
    try:
        c = category.objects.get(slug=category_slug)
        p = product.objects.filter(category=c)
    except:
        sc = subcategory.objects.get(slug=category_slug)
        p = product.objects.filter(subcategory=sc)
    
    context = {
        "products" : p,
        "title"  : category_slug,
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
    search_query = list(str(request.POST['search_query']))
    if request.POST and len(search_query) < 10 and product.objects.filter(name__icontains="".join(search_query)).count() == 0:
        search_package = product.objects.filter(Q(name__icontains=""))
        for q in search_query:
            search_package &= product.objects.filter(Q(name__icontains=str(q)))
    else:
        search_package = product.objects.filter(Q(name__icontains="".join(search_query)))
    context = {
        'title' : "".join(search_query),
        'products' : search_package,
    }
    return render(request, 'search_results', context)