"""
Render function used to serve context to
Webpages.
"""
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from .forms import public_cart_form, public_review_form
from .models import product, category, subcategory, public_reviews
from django.db.models import Q
import datetime
from django.contrib.auth import authenticate, login
from django.utils.html import strip_tags

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
#    user = None
#    if request.POST:
#        user_fetched = authenticate(username=request.POST['email'], password=request.POST['password'])
#        if user_fetched is not None:
#            login(request, user_fetched)
#        else:
#            pass
#    else:
#        pass

    c = category.objects.all()[:6]
    for i in c:
        section(i)
    s = subcategory.objects.all()[:6]
    p = product.objects.all().order_by('-name')[12:44]
    products_set_two = product.objects.all().order_by('-name')[44:56]
 
    #category_update, created =  category.objects.get_or_create(name="uncategorised")
    #for pr in p:
    #    try:
    #        m = pr.category.slug
    #    except:
    #        pr.category = category_update
    #        pr.save()

    context = {
        "products_set_one": section(category.objects.get(name__icontains="tele")),
        "products_set_two": section(category.objects.get(name__icontains="appliances")),
        "products_set_three": section(category.objects.get(name__icontains="washing")),
        "products_set_four": section(category.objects.get(name__icontains="audio")),
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
        "keywords": p.name.replace(' ', ',').split(),
        "description": strip_tags(p.detail),
        "summary": strip_tags(p.detail),
        "similar_products": similar_products,
        "meta_category": p.category.name,
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
        sc = c = subcategory.objects.get(slug=category_slug)
        p = product.objects.filter(subcategory=sc)

    context = {
        "products" : p,
        "title"  : c.name,
        "clean_description": f"Buy quality {c.name} from Mzuri Express Appliances Uganda, Enjoy shopping electronics \
          at favorable prices in Uganda",
        "keywords": f"{c.name}, mzuri, express, Uganda, electronics, wholesaler, online, shopping, \
        Uganda, in, how, much, is, electronics, shop, Kampala, price, best, machine, delivery",
        #"description": strip_tags(p.detail),
        #"summary": strip_tags(p.detail),
        "meta_category": c.name,
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
    if request.POST and len(search_query) < 30 and product.objects.filter(name__icontains="".join(search_query)).count() == 0:
        search_package = product.objects.filter(Q(name__icontains=""))
        for q in search_query:
            search_package &= product.objects.filter(Q(name__icontains=str(q)))
    else:
        search_package = product.objects.filter(Q(name__icontains="".join(search_query)))
    context = {
        'title' : "".join(search_query),
        'products' : search_package,
    }
    return render(request, 'search_results.html', context)

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
        "title": "Return and Refunds",
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
        'title': "Terms of Sale",
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
        "keywords": p.name.replace(' ', ',').split(),
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
        "keywords": p.name.replace(' ', ',').split(),
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