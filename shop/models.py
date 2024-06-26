from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

#Shop model incase of multiple branches
class shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, editable=False)
    location = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f'{self.name}'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

#Brand model
class brand(models.Model):
    """
    Product brand
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/brand_images', null=True, blank=True)
    slug = slug = models.SlugField(unique=True, editable=False)

    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

# Product rating
class rating(models.Model):
    """
    Product rating. Used to rank products.
    """
    id = models.AutoField(primary_key=True)
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.rating}'

class review(models.Model):
    """
    Reviews given by clients
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    review = models.TextField(max_length=500)
    rating = models.ForeignKey(rating, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.review}'

#Category
class category(models.Model):
    """
    Category of a product.
    Each product should have one
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(upload_to="static/category_images", null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class subcategory(models.Model):
    """
    Sub category incase a product belongs to one
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, editable=False)
    image = models.ImageField(upload_to="static/subcat_images", null=True, blank=True)
    category = models.ForeignKey(category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

# Product model
class product(models.Model):
    """
    Store product information
    """
    id = models.AutoField(primary_key=True)
    secodary_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/product_images')
    image1 = models.ImageField(upload_to='static/product_images', blank=True, null=True)
    image2 = models.ImageField(upload_to='static/product_images', blank=True, null=True)
    image3 = models.ImageField(upload_to='static/product_images', blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    brand = models.ForeignKey(brand, on_delete=models.PROTECT, null=True, blank=True)
    reviews = models.ForeignKey(review, null=True, blank=True, on_delete=models.PROTECT)
    detail = HTMLField(blank=True, null=True)
    weight = models.PositiveIntegerField()
    color = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    specifications = models.TextField(max_length=2000)
    category = models.ForeignKey(category, on_delete=models.PROTECT, null=True)
    subcategory = models.ForeignKey(subcategory, on_delete=models.PROTECT, null=True, blank=True)
    model = models.CharField(max_length=150)
    shop = models.ForeignKey(shop, on_delete=models.PROTECT, null=True, blank=True)
    items_left = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=10)
    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class category_front_page(models.Model):
    """
    Store page banners of categorical products.
    """
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='static/category_front_page', null=True, blank=True)
    category = models.ForeignKey(category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.category.name}'
    
class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.UUIDField(default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.username

"""
All user carts are in one table,
Each row represents an independent
cart item.
Pulling out cart items;
we user a user(customer_id) to get all
associated cart items.
"""
class cart(models.Model):
    customer = models.OneToOneField(customer, on_delete=models.PROTECT)
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    def __str__(self):
        return f'{self.product.name} {self.customer.user.first_name}'

"""
All check outs made by the customer
are saved here.
Will be seen by the suppliers
"""   
class order(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.PROTECT)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    cart = models.OneToOneField(cart, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.customer.user.first_name