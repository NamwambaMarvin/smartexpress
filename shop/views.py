"""
Render function used to serve context to
Webpages.
"""
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
import random
from .forms import public_cart_form, public_review_form
from .models import product, category, subcategory, public_reviews
from django.db.models import Q
import datetime
import decimal
from django.contrib.auth import authenticate, login
from django.utils.html import strip_tags

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
    p = product.objects.all().order_by('-name')[12:44]

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
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.product_name = request.POST["product_name"]
            new_form.product_id = request.POST["product_id"]
            new_form.save()
            return redirect(reverse("shop:order_success"))
        else:
            return redirect(reverse("shop:order_failed"))

def public_review(request):
    if request.method == "POST":
        review_form = public_review_form(request.POST)
        if review_form.is_valid():
            new_review_form = review_form.save(commit=False)
            new_review_form.product_sec_id = request.POST["product_sec_id"]
            new_review_form.product_id = request.POST["product_id"]
            new_review_form.product_name = request.POST["product_name"]
            new_review_form.save()
            return redirect(reverse("shop:review_success"))
        else:
             return redirect(reverse("shop:review_failed"))
    else:
        pass
        

def single_product(request, category_slug, product_slug):
    """
    This displays details of a product in a particular category
    """
    form = public_cart_form()
    review_form = public_review_form()
    try:
        c = category.objects.get(slug=category_slug)
        p = product.objects.get(slug=product_slug, category=c)
        similar_products =  product.objects.filter(brand=p.brand)
        title = p.name
    except:
        c = None
        p = product.objects.get(slug=product_slug)
        title = "No Product Found"

    percentage_discount = p.discount*100
    percentage_discount = percentage_discount/p.price
    original_price = p.price+p.discount

    context = {
        "title"  : title,
        "product" : p,
        "original_price": original_price,
        "form": form,
        "review_form": review_form,
        "percentage_discount": percentage_discount,
        "clean_description": strip_tags(p.detail),
        "similar_products": similar_products,
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

def shipping_and_delivery_policy(request):
    context = {
        'title': 'Shipping and Delivery Policy'
    }
    return render(request, 'shipping_and_delivery_policy.html', context)

def contact(request):
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'contact.html', context)

def terms(request):
    context = {
        'title': 'Terms and Conditions'
    }
    return render(request, 'terms_and_conditions.html', context)

def about(request):
    context = {
        'title': 'About Mzuri Express'
    }
    return render(request, 'about.html', context)

def order_success(request):
    context = {
    }
    return render(request, 'order_success.html', context)

def order_failed(request):
    context = {
    }
    return render(request, 'order_failed.html', context)

def review_success(request):
    context = {
    }
    return render(request, 'review_success.html', context)

def review_failed(request):
    context = {
    }
    return render(request, 'review_failed.html', context)

def return_and_refunds_policy(request):
    context = {
        "title": "Return and Refunds",
    }
    return render(request, 'return_and_refund.html', context)

def privacy_policy(request):
    context = {
        'title': "Privacy policy",
    }
    return render(request, 'privacy_policy.html', context)

def terms_of_sale(request):
    context = {
        'title': "Terms of Sale",
    }
    return render(request, 'terms_of_sale.html', context)