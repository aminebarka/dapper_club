from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .models import Order
from .forms import OrderForm
from django.conf import settings
from accounts.models import UserProfile
import datetime
import razorpay



# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))






# Create your views here.
def place_order(request):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    total_amount = 0
    for cart_item in cart_items:
        total_amount += (cart_item.product.product.price * cart_item.quantity)

    tax = round((5 * float(total_amount))/100)
    sub_total = total_amount - tax
    coupon_discount = 0

    if request.method == 'POST':
        print("hai")
        form = OrderForm(request.POST) 
        print("hai")
        if form.is_valid():

            #storing user address in user_profile table
            if not UserProfile.objects.filter(user=request.user):
                user_profile = UserProfile()
                user_profile.user = request.user
                user_profile.address_line_1 = form.cleaned_data['address_line_1']
                user_profile.address_line_2 = form.cleaned_data['address_line_2']
                user_profile.country = form.cleaned_data['country']
                user_profile.state = form.cleaned_data['state']
                user_profile.city = form.cleaned_data['city']
                user_profile.save()

            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.payment_method = form.cleaned_data['payment_method']  
            data.order_total = total_amount
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            payment_mode = form.cleaned_data['payment_method']

            if data.coupon:
                coupon_discount = data.coupon_discount
                total_amount = data.order_total
            context = {
                'order': order,
                'cart_items': cart_items,
                'sub_total': sub_total,
                'tax': tax,
                'total_amount': total_amount,
                'payment_mode':payment_mode,
                'coupon_discount':coupon_discount
            }
            return render(request, 'orders/payment.html', context)

        
    return redirect('checkout')


def cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    # print(razorpay_client)
    # print(order.payment_method)
    # if order.payment_method == 'razorpay':
    #     payment_id = order.payment.payment_id
    #     print(payment_id)
    #     razorpay_client.payment.refund(payment_id,{
    #         "amount": "100",
    #         "speed": "normal",
    #         "notes": {
    #             "notes_key_1": "Beam me up Scotty.",
    #             "notes_key_2": "Engage"
    #         },
    #         "receipt": "Receipt No. 31"
    #         })
    #     order.refund_status = 'Processing'
    #     print("hai")
    order.status = 'Cancelled'
    order.save()
    print("sett")

    return redirect('my_order')