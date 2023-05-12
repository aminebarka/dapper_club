from .models import Category, Brand, Size, Color, PriceFilter
from carts.models import CartItem, WishlistItem, Cart
from store.models import Product, ProductAttribute



def get_filters(request):
    if not request.session.session_key:
            request.session.create()
    cats = Category.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all().order_by('id')
    prices = PriceFilter.objects.all()
    prods = Product.objects.all()
    cart_count = 0
    wished_count = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
        wished_items = WishlistItem.objects.filter(user= request.user)
        wished_count = wished_items.count()

    else:
        if Cart.objects.filter(cart_id=request.session.session_key):
            cart = Cart.objects.get(cart_id=request.session.session_key)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = cart_items.count()
        wished_count = 0

    data = {
        'cats':cats,
        'brands':brands,
        'colors':colors,
        'sizes':sizes,
        'prods':prods,
        'prices':prices,
        'cart_count':cart_count,
        'wished_count':wished_count,
    }
    return data