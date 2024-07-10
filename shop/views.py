"""
Render function used to serve context to
Webpages.
"""
from django.shortcuts import render, redirect, HttpResponse
import random
from .forms import public_cart_form
from .models import product, category, subcategory, rating, brand, category_front_page
from django.db.models import Q
import datetime
from django.contrib.auth import authenticate, login

# Make query sets random
# 1D query set
def _shuffle(query_set):
    new_list = []
    for i in query_set:
        new_list.append(i)
    random.shuffle(new_list)
    return new_list

# Create your views here.
def index(request):
    """
    View serving the home page logic
    """
    user = None
    if request.POST:
        user_fetched = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user_fetched is not None:
            login(request, user_fetched)
        else:
            pass
    else:
        pass

    c = category.objects.all()[:6]
    s = subcategory.objects.all()[:12]
    p = product.objects.all()[12:44]

    category_update, created =  category.objects.get_or_create(name="uncategorised")
    for pr in p:
        try:
            m = pr.category.slug
        except:
            pr.category = category_update
            pr.save()

    context = {
        "products": _shuffle(p),
        "subcategories" : _shuffle(s),
        "category": _shuffle(c),
        "title"  : "shop",
        'last_revised': datetime.datetime.today(),
        'meta_category': "PRODUCTS",
        'summary': "Shop home appliances, electronics and other products with mzuri express",
        'keywords': "shopping, mzuriexpress, mzuri, express, online store",
        'description': "Mzuri express offers a wide variety of products made from around the planet, Start shopping on the fly",
    }
    return render(request, 'index', context)

def shop_home(request, shop_name):
    return render(request, 'index', {})

def public_cart(request):
    if request.method == "POST":
        form = public_cart_form(request.POST)
        form
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product_name = request.POST["product_name"]
            new_form.product_id = request.POST["product_id"]
            new_form.save()
            return redirect("/")
        else:
            pass


def single_product(request, category_slug, product_slug):
    """
    This displays details of a product in a particular category
    """
    form = public_cart_form()
    try:
        c = category.objects.get(slug=category_slug)
        p = product.objects.get(slug=product_slug, category=c)
        title = p.name
    except:
        c = None
        p = product.objects.get(slug=product_slug)
        title = "No Product Found"

    context = {
        "title"  : title,
        "product" : p,
        "form": form,
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