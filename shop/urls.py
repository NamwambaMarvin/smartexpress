from django.conf import settings
from django.conf.urls.static import static
# Import path
from django.contrib import admin
from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/<slug:shop_name>/', views.shop_home, name='shop_home'),
    path('search/', views.search, name='search'),
    path('public_cart/', views.public_cart, name='public_cart'),
    path('products/<slug:category_slug>/', views.products, name='products'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.single_product, name='single_product'),
    path('subproduct/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.subproducts, name='subproducts'),
    path('shipping_and_delivery/', views.shipping_and_delivery_policy, name='shipping'),
    path('contact/', views.contact, name='contact'),
    path('terms_and_conditions/', views.terms, name='terms'),
    path('about_us/', views.about, name='about'),
    path('public_review/', views.public_review, name='public_review'),
    path('order_success/', views.order_success, name='order_success'),
    path('order_failed/', views.order_failed, name='order_failed'),
    path('review_failed/', views.review_failed, name='review_failed'),
    path('review_success/', views.review_success, name='review_success'),
    path('terms_of_sale/', views.terms_of_sale, name='terms_of_sale'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('return_and_refunds/', views.return_and_refunds_policy, name='return_and_refunds'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)