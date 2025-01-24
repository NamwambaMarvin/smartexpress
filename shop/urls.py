from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from shop.models import product
# Import path
from django.urls import path
from . import views

app_name = "shop"

products = {
    "queryset": product.objects.all(),
    "date_field": "updated_at",
}

urlpatterns = [
    path('products/<slug:category_slug>/', views.products, name='products'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.single_product, name='single_product'),
    path('product/<slug:product_slug>/', views.single_product_slug, name='single_product_slug'),
    path('product/<slug:subcategory_slug>/<slug:product_slug>/', views.subproducts, name='subproducts'),
    # Cleaner URL remapping
    path('', views.index, name='index'),
    path('shop/<slug:shop_name>/', views.shop_home, name='shop_home'),
    path('public_cart/', views.public_cart, name='public_cart'),
    path('search/', views.search, name='search'),
    path('shipping_and_delivery/', views.shipping_and_delivery_policy, name='shipping'),
    path('shipping_policy/', views.shipping_and_delivery_policy, name='shipping_policy'),
    path('contact/', views.contact, name='contact'),
    path('terms_and_conditions/', views.terms, name='terms'),
    path('about_us/', views.about, name='about'),
    path('public_review/', views.public_review, name='public_review'),
    path('order_success/', views.order_success, name='order_success'),
    path('order_failed/', views.order_failed, name='order_failed'),
    path('review_failed/', views.review_failed, name='review_failed'),
    path('review_success/', views.review_success, name='review_success'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('return_and_refunds/', views.return_and_refunds_policy, name='return_and_refunds'),
    path('return_policy/', views.return_and_refunds_policy, name='return_policy'),
    path('sign_up/', views.sign_up, name='sign_up'),
    #path('<slug:product_slug>/', views.single_product_slug, name='single_product_slug'),
    path('product/<uuid:product_uuid>/', views.uuid_product_single, name='uuid_product_single'),
    path('category/<slug:category_slug>/', views.products, name='products'),
    path('place-order/<slug:product_slug>/', views.request_call, name='request_call'),
    path('review/<slug:product_slug>/', views.review, name='review'),
    path('cookie_policy/', views.cookie_policy, name='cookie_policy'),
    # Site map
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"products": GenericSitemap(products, priority=0.8, changefreq="weekly")}},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)