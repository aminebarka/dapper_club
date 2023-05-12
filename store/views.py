from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, ProductAttribute, ReviewRating
from accounts.models import UserProfile
from category.models import Category, Brand, Color, Size, PriceFilter
from carts.models import Cart, CartItem, WishlistItem
from orders.models import OrderProduct
from .forms import ReviewForm
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def store(request, category_slug=None) :
    categories = None
    products = None
    print(category_slug)

    if category_slug != None:

        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(sub_category__category=categories) 
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()


    else:
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()


    context = {
        'products': paged_products,
        'products_count':products_count,

    }
    return render(request, 'store/shop.html', context)


def product_detail(request, sub_category_slug, product_slug):

    print("hai product", product_slug)

    if not request.session.session_key:
        request.session.create()
    try: 
        product = Product.objects.get(slug=product_slug)
        related_products = Product.objects.filter(sub_category__category=product.sub_category.category).exclude(slug=product_slug)[:4]
        colors=ProductAttribute.objects.filter(product=product).values('color__id','color__name','color__color_code').distinct()
        sizes=ProductAttribute.objects.filter(product=product).values('id','size__id','size__size','color__id', 'stock').distinct()
        price = ProductAttribute.objects.filter(product=product).first()
        in_wishlist = None
        if request.user.is_authenticated:
            in_wishlist=WishlistItem.objects.filter(user=request.user, product=product)
        

    except Exception as e:
        raise e


    try:
        is_ordered = OrderProduct.objects.filter(user=request.user, product__product=product).exists()

    except:
        is_ordered = None

    # show the reviews
    reviews = ReviewRating.objects.filter(product=product, status=True)
    context = {
   
        'related':related_products,
        'product':product,
        'sizes':sizes,
        'colors':colors,
        'price':price,
        'in_wishlist':in_wishlist,
        'is_ordered':is_ordered,
        'reviews':reviews

    }
    print("hai 6")
    return render(request, 'store/product_detail.html', context)


def store_by_brand(request, brand_slug=None):
    
    print("brand")
    products = None
    brands = None

    print("hai")
    brands = get_object_or_404(Brand, slug=brand_slug)
    print("helllo")

    products = Product.objects.filter(brand = brands).order_by('-id')
    print("pooi")
    products_count = products.count()

    context = {
        'products': products,
        'products_count':products_count,

    }
    return render(request, 'store/shop.html', context)


def search(request):
    q = request.GET['q']
    products = Product.objects.filter(product_name__icontains=q, sub_category__category__category_name__icontains=q).order_by('-id')
    products_count = products.count()
    context = {
        'products': products,
        'products_count':products_count,
        # 'brands':brands,

    }
    return render(request, 'store/search.html', context)


def product_by_color(request, color_slug):
    colors = get_object_or_404(Color, slug=color_slug)

    products = Product.objects.filter(productattribute__color=colors).distinct()
    products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/shop.html', context)


def product_by_size(request, size_slug):
    sizes = get_object_or_404(Size, slug=size_slug)
    print(sizes)

    products = Product.objects.filter(productattribute__size=sizes).distinct()
    
    products_count = products.count()
    context = {
        'products':products, 
        'products_count':products_count,
    }
    return render(request, 'store/shop.html', context)


def products_by_price(request, price_id):
    price_filter = get_object_or_404(PriceFilter, id=price_id)
    products = Product.objects.filter(price_filter=price_filter).order_by('price')
    products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/shop.html', context)


def price_hightolow(request):
    products = Product.objects.all().order_by('price')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()

    context = {
        'products' : paged_products,
        'products_count' : products_count
    }
    return render(request, 'store/shop.html', context)


def price_lowtohigh(request):
    products = Product.objects.all().order_by('-price')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()

    context = {
        'products' : paged_products,
        'products_count' : products_count
    }
    return render(request, 'store/shop.html', context)
    


@login_required(login_url='signin')
def checkout(request):
    context = {}
    user=request.user
    cart_items=CartItem.objects.filter(user=user, is_active=True)
    userprofile = UserProfile.objects.filter(user=request.user).first()
    
    total_amount = 0
    for cart_item in cart_items:

        total_amount += (cart_item.product.product.price * cart_item.quantity)


    tax = round((5 * float(total_amount))/100)
    sub_total = total_amount - tax
    context = {
        'total_amount':total_amount,
        'tax':tax,
        'sub_total':sub_total,
        'cart_items':cart_items,
        'userprofile':userprofile
        # 'single_product':request.session['cartdata']
    }
    return render(request, 'store/checkout.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    print("hai")
    if request.method == 'POST':
        try:
            print("hai2")

            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            print("hai3")

            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating() 
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                print("ha6i")

                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)





