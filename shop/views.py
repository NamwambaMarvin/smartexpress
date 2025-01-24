"""
Render function used to serve context to
Webpages.
"""
from functools import reduce
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from .forms import public_cart_form, public_review_form
from .models import product, category, subcategory, public_reviews
from django.db.models import Q
import datetime
import random
from django.contrib.auth import authenticate, login
from django.utils.html import strip_tags
from .forms import RegisterForm
from django.utils.text import slugify

class section:
    def __init__(self, category):
        self.name = category.name
        self.products = category.product_set.all()[:4]
        self.products_set_two = category.product_set.all()[4:8]
        self.id = category.id
        self.slug = category.slug

# Create your views here.
def index(request):
    """
    View serving the home page logic
    """
    c = subcategory.objects.all()[6:12]
    for i in c:
        section(i)
    s = subcategory.objects.all()[:6]
    p = product.objects.all().order_by('-name')[12:44]
    products_set_two = product.objects.all().order_by('-name')[44:56]

    context = {
        "products_set_one": section(subcategory.objects.get(id=1)),
        "products_set_two": section(subcategory.objects.get(id=2)),
        "products_set_three": section(subcategory.objects.get(id=3)),
        "products_set_four": section(subcategory.objects.get(id=4)),
        "subcategories" : s,
        "category": c,
        "title"  : "Mzuri Express Appliances Uganda",
        'last_revised': datetime.datetime.today(),
        'meta_category': "PRODUCTS",
        'summary': "Shop home appliances, electronics and other products with Mzuri Express Appliances Uganda",
        'keywords': "shopping, mzuriexpress, mzuri, express, online store, uganda, online shopping",
        'description': "Mzuri Express Appliances Uganda offers a variety of electronic products. Buy Televisions, fridges, cookers, Ovens, Dispensers, Washing machines, freezers, Blenders, Air Conditioners, Sound Bars, Electronic Kettles and many more",
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
    
class psection:
    def __init__(self, subject_product):
        """
        Accept a product, and get related products using
        its properties
        """
        self.name = "Other " + subject_product.subcategory.name
        products = product.objects.filter(subcategory=subject_product.subcategory)
        starting_point = random.randint(0, products.count()-4)
        self.products = products[starting_point:starting_point+4]
        self.products_set_two = product.objects.filter(subcategory=subject_product.subcategory)[4:8]
        self.id = subject_product.slug
        self.slug = subject_product.subcategory.slug

def single_product(request, category_slug, product_slug):
    """
    This displays details of a product in a particular category
    """

    form = public_cart_form()
    review_form = public_review_form()
    similar_products = None
    try:
        c = category.objects.get(slug=category_slug)
        p = product.objects.get(slug=product_slug, category=c)
        title = p.name
        # Get a product that is in the same category and brand as the current product
        try:
            similar_products = psection(p)
        except:
            similar_products = None
        
    except:
        c = None
        p = product.objects.get(slug=product_slug)
        title = p.name
        # Get a product that is in the same category and brand as the current product
        try:
            similar_products = psection(p)
        except:
            similar_products = None

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
        "keywords": ", ".join(slugify(p.name).split("-")),
        "description": strip_tags(p.detail),
        "summary": strip_tags(p.detail),
        "meta_category": p.category.name,
        "similar_products": similar_products,
    }
    return render(request, 'product', context)

def products(request, category_slug):
    """
    This displays products in a particular category.
    """
    # Try to fetch products in
    # either a category or sub category
    try:
        c = subcategory.objects.get(slug=category_slug)
        p = product.objects.filter(subcategory=c)[:13]
    except:
        sc = c = category.objects.get(slug=category_slug)
        p = product.objects.filter(category=sc)[:13]

    context = {
        "products" : p,
        "title"  : c.name,
        "description": f"Buy quality {c.name} from Mzuri Express Appliances Uganda, Enjoy shopping electronics at favorable prices in Uganda",
        "keywords": f"{c.name}, mzuri, express, Uganda, electronics, wholesaler, online, shopping, Uganda, in, how, much, is, electronics, shop, Kampala, price, best, machine, delivery",
        #"description": strip_tags(p.detail),
        #"summary": strip_tags(p.detail),
        "meta_category": c.name,
    }
    return render(request, 'products', context)

def subproducts(request, subcategory_slug, product_slug):
    """
    This displays products in a subcategory
    """
    """
    This displays details of a product in a particular category
    """
    form = public_cart_form()
    review_form = public_review_form()
    try:
        c = subcategory.objects.get(slug=subcategory_slug)
        p = product.objects.get(slug=product_slug, subcategory=c)
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
        "keywords": ", ".join(slugify(p.name).split("-")),
        "description": strip_tags(p.detail),
        "summary": strip_tags(p.detail),
        "similar_products": similar_products,
        "meta_category": p.category.name,
    }
    context = {
        "title" : "product_detail",
    }
    return render(request, 'product', context=context)

def search(request):
    """
    To search products from the database
    """
    # Turn everything in the search query into a string
    search_query = str(request.GET['search_query'])

    if len(search_query) > 300:
        search_query = ""

    # Remove all delimiters from the string
    # and make it a list
    no_space = search_query.split()

    # Strip the number of search words to 30
    if len(no_space) > 30:
        no_space = no_space[:30]

    search_package = product.objects.filter(name="APPLE")
    if len(no_space) <= 1:
       search_package = product.objects.filter(
            Q(name__icontains=no_space[0])
        )
    else:
        search_package = product.objects.filter(
            reduce(
                lambda x, y: x & y, [Q(name__icontains=word) for word in no_space]
                )
            )

    context = {
        'title' : "".join(search_query),
        'products' : search_package,
    }
    return render(request, 'search_results.html', context)

def shipping_and_delivery_policy(request):
    context = {
        'title': 'Shipping Policy'
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
        'title': 'About Mzuri Express Appliances Uganda'
    }
    return render(request, 'about.html', context)

def order_success(request):
    context = {
        'title': 'Order Success'
    }
    return render(request, 'order_success.html', context)

def order_failed(request):
    context = {
        'title': 'Order Failed'
    }
    return render(request, 'order_failed.html', context)

def review_success(request):
    context = {
        'title': 'Review Success'
    }
    return render(request, 'review_success.html', context)

def review_failed(request):
    context = {
        'title': 'Review Failed'
    }
    return render(request, 'review_failed.html', context)

def return_and_refunds_policy(request):
    context = {
        "title": "Return Policy",
    }
    return render(request, 'return_and_refund.html', context)

def privacy_policy(request):
    context = {
        'title': "Privacy policy",
    }
    return render(request, 'privacy_policy.html', context)

def cookie_policy(request):
    context = {
        'title': "Cookie policy",
    }
    return render(request, 'cookie_policy.html', context)

def terms_of_sale(request):
    context = {
        'title': "Terms and Conditions",
    }
    return render(request, 'terms_of_sale.html', context)

def sign_up(request):
    context = {
        'title': "Sign Up",
    }
    return render(request, 'sign_up.html', context)

# Fetches the product using its uuid
def uuid_product_single(request, product_uuid):
    """
    This displays details of a product in a particular category
    """
    form = public_cart_form()
    review_form = public_review_form()
    try:
        p = product.objects.get(secodary_id=product_uuid)
        title = p.name
    except:
        c = None
        p = product.objects.get(secodary_id=product_uuid)
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
        "keywords": ", ".join(slugify(p.name).split("-")),
        "description": strip_tags(p.detail),
        "summary": strip_tags(p.detail),
        "meta_category": p.category.name,
    }
    return render(request, 'product', context)

# Fetches the product using its slug
def single_product_slug(request, product_slug):
    """
    This displays details of a product in a particular category
    """
    form = public_cart_form()
    review_form = public_review_form()
    try:
        p = product.objects.get(slug=product_slug)
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
        "keywords": ", ".join(slugify(p.name).split("-")),
        "description": strip_tags(p.detail),
        "summary": strip_tags(p.detail),
        "meta_category": p.category.name,
    }
    return render(request, 'product', context)


def request_call(request, product_slug):
    form = public_cart_form()
    try:
        p = product.objects.get(slug=product_slug)
        title = p.name
    except:
        c = None
        p = product.objects.get(slug=product_slug)

    context = {
        "product" : p,
        "form": form,
    }
    return render(request, 'request_call.html', context)

def review(request, product_slug):
    review_form = public_review_form()
    try:
        p = product.objects.get(slug=product_slug)
        title = p.name
    except:
        c = None
        p = product.objects.get(slug=product_slug)

    context = {
    "product" : p,
    "review_form": review_form,
}
    return render(request, 'review_product.html', context)

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/category/blenders/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})


def other_products(request, category_slug):
    """
    This displays products in a particular category
    """
    # Try to fetch products in
    # either a category or sub category
    try:
        c = subcategory.objects.get(slug=category_slug)
        p = product.objects.filter(subcategory=c)[:13]
    except:
        sc = c = category.objects.get(slug=category_slug)
        p = product.objects.filter(category=sc)[:13]

    context = {
        "products" : p,
        "title"  : c.name,
        "description": f"Buy quality {c.name} from Mzuri Express Appliances Uganda, Enjoy shopping electronics at favorable prices in Uganda",
        "keywords": f"{c.name}, mzuri, express, Uganda, electronics, online, shopping, Uganda, in, how, much, is, electronics, shop, Kampala, price, best, machine, delivery",
        #"description": strip_tags(p.detail),
        #"summary": strip_tags(p.detail),
        "meta_category": c.name,
    }
    return render(request, 'products', context)