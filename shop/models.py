from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

#Shop model incase of multiple branches
class shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = slugify(name)
    shop_location = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.name}'

#Brand model
class brand(models.Model):
    """
    Product brand
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/brand_images')
    slug = slugify(name)

    def __str__(self) -> str:
        return f'{self.name}'

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
    rating = models.ForeignKey(rating, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.review}'

#Category
class category(models.Model):
    """
    Category of a product.
    Each product should have one
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    slug = slugify(name)
    image = models.ImageField(upload_to="static/category_images")

    def __str__(self) -> str:
        return f'{self.name}'

class subcategory(models.Model):
    """
    Sub category incase a product belongs to one
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = slugify(name)
    image = models.ImageField(upload_to="static/subcat_images")
    category = models.ForeignKey(category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.name}'

# Product model
class product(models.Model):
    """
    Store product information
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/product_images')
    slug = slug = slugify(name)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    brand = models.ForeignKey(brand, on_delete=models.PROTECT)
    reviews = models.ForeignKey(review, null=True, blank=True, on_delete=models.PROTECT)
    detail = models.TextField(max_length=3000)
    weight = models.PositiveIntegerField()
    color = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    specifications = models.TextField(max_length=2000)
    category = models.ForeignKey(category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(subcategory, on_delete=models.PROTECT)
    model = models.CharField(max_length=50)
    shop = models.ForeignKey(shop, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

class category_front_page(models.Model):
    """
    Store page banners of categorical products.
    """
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='static/category_front_page')
    category = models.ForeignKey(category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.category.name}'