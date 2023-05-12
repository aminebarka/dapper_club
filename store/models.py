from autoslug import AutoSlugField
from category.models import *
from accounts.models import Account
from django.db import models
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from django.db.models import Avg, Count
# Create your models here.

class Product(models.Model):
    product_name           = models.CharField(max_length=200, unique=True)
    slug                   = AutoSlugField(populate_from='product_name', unique=True, null=True, default=None)
    description            = models.TextField(max_length=500, unique=True)
    image1                 = models.ImageField(upload_to='photos/products')
    image2                 = models.ImageField(upload_to='photos/products', null=True, blank=True)
    image3                 = models.ImageField(upload_to='photos/products', null=True, blank=True)
    image4                 = models.ImageField(upload_to='photos/products', null=True, blank=True)
    sub_category           = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand                  = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price                  = models.IntegerField(default=None, null=True)
    price_filter           = models.ForeignKey(PriceFilter, on_delete=models.CASCADE, null=True, blank=True)
    is_available           = models.BooleanField(default=True)
    is_featured            = models.BooleanField(default=False)
    created_date           = models.DateTimeField(auto_now_add=True)
    modified_date          = models.DateTimeField(auto_now=True)

 
    def get_url(self):
        return reverse('product_detail', args=[self.sub_category.slug, self.slug])


    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image1.url)) 
        

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ProductAttribute(models.Model):
    product                = models.ForeignKey(Product, on_delete=models.CASCADE)
    # image                 = models.ImageField(upload_to='photos/products',null=True)
    color                  = models.ForeignKey(Color, on_delete=models.CASCADE)
    size                   = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock                  = models.IntegerField()
    is_available           = models.BooleanField(default=True)
    created_date           = models.DateTimeField(auto_now_add=True)
    modified_date          = models.DateTimeField(auto_now=True)

    #     created_date           = models.DateTimeField(auto_now_add=True)
    # modified_date          = models.DateTimeField(auto_now=True)


    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.product.image1.url))


    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s" ></div>' % (self.color.color_code))


    def __str__(self):
        return self.product.product_name



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject