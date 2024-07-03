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
    path('products/<slug:category_slug>/', views.products, name='products'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.single_product, name='single_product'),
    path('subproduct/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.subproducts, name='subproducts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)