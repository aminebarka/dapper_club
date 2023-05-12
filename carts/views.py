from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import JsonResponse
from store.models import Product, ProductAttribute
from orders.models import Order
from .models import Cart, CartItem,WishlistItem, Coupon
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone




# Create your views here.




#Add To Cart

def add_to_cart(request):

    current_user=request.user
    product = ProductAttribute.objects.get(id__exact=request.GET['id'])
    try:
        cart = Cart.objects.get(cart_id = request.session.session_key)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = request.session.session_key)
        cart.save()
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user).update(quantity=request.GET['qty'])
            return JsonResponse({'status':"Cart updated"})

        else:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = request.GET['qty'],
                    user = current_user,
                )
            return JsonResponse({'status':"Item added to cart"})

    else:
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:

            CartItem.objects.filter(product=product, cart=cart).update(quantity=request.GET['qty'])
            return JsonResponse({'status':"Cart updated"})

        else:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = request.GET['qty'],
                    cart = cart,
                )
            return JsonResponse({'status':"Item added to cart"})


def cart(request):
    print("ha ca")
    current_user=request.user
    context = {}
    try:
        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(user=current_user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=request.session.session_key)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

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
            # 'single_product':request.session['cartdata']
        }
        print("ha cart0000000000")
    except:
        print("hao")
        pass #just ignore
    
    return render(request, 'store/cart.html', context)

# delete cart item

def cart_delete(request, prod_id):
    # p_id = str(request.GET['id'])
    current_user=request.user 
    product = get_object_or_404(ProductAttribute, id=prod_id)
    if current_user.is_authenticated:
        cart_item=CartItem.objects.get(user=current_user, product=product)
    else:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    print("ha cart")
    return redirect('cart')

# update cart item 

def cart_update(request):
    current_user=request.user
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    product = get_object_or_404(ProductAttribute, id=p_id)
    if current_user.is_authenticated:
        cart_item=CartItem.objects.get(user=current_user, product=product)
    else:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity = p_qty
    cart_item.save()


    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)

    else:
        cart = Cart.objects.get(cart_id=request.session.session_key)

        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

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
        }
    t = render_to_string('store/ajax/cart-list.html', context)
    return JsonResponse({'data':t, 'status':'cart updated successfully'})

@login_required(login_url='signin')
def add_to_wishlist(request):
    user = request.user
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print(user, product)
    is_wished = WishlistItem.objects.filter(product=product)
    if not is_wished:
        print("yes")
        product = WishlistItem.objects.create(
            user=user,
            product=product,
            is_active=True,
        )
        message = 'Item added to wishlist'
        status = 'success'
    
    else:
        print("no")

        message = 'Item already in wishlist'
        status = 'fail'
    
    return JsonResponse({'message':message, 'status': status})


@login_required(login_url='signin')
def wishlist(request):
    products = WishlistItem.objects.filter(user=request.user, is_active=True)

    return render(request, 'store/wishlist.html', {'products':products})


def delete_from_wishlist(request):
    prod_id = request.GET['id']
    print(prod_id)
    product = Product.objects.get(id=prod_id)
    wishlist_item = WishlistItem.objects.get(product=product)
    wishlist_item.delete()
    return JsonResponse({'status':'item removed'})


def apply_coupon(request):
    coupon_code = request.GET['coupon_code']
    if Coupon.objects.filter(coupon_code__exact=coupon_code, is_active=True).exists():
        coupon = Coupon.objects.filter(coupon_code__exact=coupon_code, is_active=True)
        order = Order.objects.get(order_number=request.GET['order_number'])
        if not Order.objects.filter(user=request.user, coupon=coupon[0], is_ordered=True):
            if coupon.filter(expiry_date__gte=timezone.now()):
                if order.order_total > coupon[0].minimum_amount:
                    order.coupon = coupon[0]
                    order.coupon_discount = coupon[0].discount_price
                    order.order_total -= coupon[0].discount_price
                    order.save()
                    messages ="Coupon applied successfully"

                    current_user = request.user
                    cart_items = CartItem.objects.filter(user=current_user)
                    total_amount = 0
                    for cart_item in cart_items:
                        total_amount += (cart_item.product.product.price * cart_item.quantity)

                    tax = round((5 * float(total_amount))/100)
                    sub_total = total_amount - tax
                    coupon_discount = order.coupon_discount
                    total_amount -= coupon_discount
                    context = {
                    'order': order,
                    'cart_items': cart_items,
                    'sub_total': sub_total,
                    'tax': tax,
                    'total_amount': total_amount,
                    'payment_mode':order.payment_method,
                    'coupon_discount':coupon_discount
                }
                    t = render_to_string('orders/ajax/payment_ajax.html', context)
                    return JsonResponse({'data':t, 'msg':messages})

                else:
                    messages="You minimum amount of "+coupon.minimum_amount+" to avail this coupon!"
                    return JsonResponse({'msg':messages})



            else:
                messages = "Coupon expired!"
                return JsonResponse({'msg':messages})

        else:
            messages = "You already applied this Coupon!"
            return JsonResponse({'msg':messages})


    else:
        messages = "Coupon does not exists!"
        return JsonResponse({'msg':messages})