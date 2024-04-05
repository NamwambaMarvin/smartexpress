from django.conf import settings
from django.conf.urls.static import static
# Import path
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('search/<str:search_query>/', views.search, name='search'),
    path('products/<slug:category_slug>/', views.products, name='products'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('subproduct/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.subproducts, name='subproducts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)