from django.shortcuts import get_object_or_404, render
from store.models import Product, ProductAttribute
from category.models import Category, Brand
from .models import Banner


# Create your views here.
def index(request):
    banners = Banner.objects.all().order_by('-id')
    products = Product.objects.filter(is_featured=True).order_by('-id')
    context = {
        'products':products,
        'banners':banners,
    }
    
    return render(request, 'home/index.html', context)


