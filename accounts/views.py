from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Account, UserProfile
from .forms import RegistrationForm, UserProfileForm, UserForm
from carts.models import Cart, CartItem
from orders.models import OrderProduct, Order
import requests

#  verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# mobile_otp
from .otp_verification import *


# Create your views here.

# new user registration
def register(request):

    # returning to home page if user is already signed
    if request.user.is_authenticated:
        return redirect('index')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, phone_number=phone_number, password=password)
            user.save()

            # user activation using email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messaage = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_mail = email
            send_male = EmailMessage(mail_subject, messaage, to=[to_mail])
            send_male.send()
            
            messages.success(request, "Activation email is sent to your email. Please activate your account")
            return redirect('register')

    context = {'form':form}
    return render(request, 'accounts/register.html', context) 


# user activation email verification
def activate_email(request,uidb64, token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account.objects.get(pk=uid) 

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        user_verifcation=VerificationUser()
        user_verifcation.user=user
        user_verifcation.email_verification=True
        user_verifcation.save()
        messages.success(request, 'Account registered succesfully. Please to signin...')
        return redirect('signin')
    else:
        messages.error(request, 'Link expired! Please try again ..')
        return redirect('register')


# user signin
def signin(request):

    # returning to home page if user is already signed
    if request.user.is_authenticated:
        return redirect('index')

    form = RegistrationForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password = password )
        if user is not None:
                # checking if there have any products in cart adding to user
                if Cart.objects.filter(cart_id=request.session.session_key):
                    cart = Cart.objects.get(cart_id = request.session.session_key)
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    # checking if there have same product for user in cart
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        products = []
                        qty = []
                        for item in cart_item:
                            product = item.product
                            products.append(product)
                            qty.append(item.quantity)
                        cart_item = CartItem.objects.filter(user=user)
                        ex_product_list = []
                        id = []
                        for item in cart_item:
                            existing_product = item.product
                            ex_product_list.append(existing_product)
                            id.append(item.id)
                        # if there have same product in user cart, updating it's quantity
                        for pr in products:
                            index = products.index(pr)
                            item_qty = qty[index]
                            if pr in ex_product_list:
                                print(pr)
                                index = ex_product_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity = item_qty
                                item.user = user
                                item.save()
                            # if there is no same product in user's cart adding it
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                # user login
                login(request, user)
                # redirecting user to the same page after login if user trying to login from another pages
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('index')
        else:
            messages.error(request, "Invalid login credentials")

    
    context = {'form':form}
    return render(request, 'accounts/signin.html', context)

# user sign out
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, "Logged out Succesfully")
    return redirect('signin')


# user dashboard
@login_required(login_url='signin')
def dashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    order_count = orders.count()
    context = {
        'orders':orders,
        'order_count':order_count,
    }
    return render(request, 'accounts/user_dashboard/dashboard.html', context)


#user orders
@login_required(login_url='signin')
def my_order(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-id')
    context = {
        'orders':orders,
    }
    return render(request, 'accounts/user_dashboard/my_orders.html', context) 



# user order details
@login_required(login_url='signin')
def order_detail(request, order_id):
    print(order_id)
    order = Order.objects.get(order_number=order_id)
    ordered_products = OrderProduct.objects.filter(order=order)
    total_amount = 0
    for item in ordered_products:
        total_amount += (item.product_price * item.quantity)
    tax = round((5 * float(total_amount))/100)
    sub_total = total_amount - tax
    coupon_discount = order.coupon_discount
    total_amount -= coupon_discount
    context = {
        'order':order,
        'ordered_products':ordered_products,
        'sub_total':sub_total,
        'tax':tax,
        'coupon_discount':coupon_discount,
        'total_amount':total_amount,
    }
    return render(request, 'orders/order_detail.html', context)


# user profile details
@login_required(login_url='signin')
def my_profile(request):
    if UserProfile.objects.filter(user=request.user):
        userprofile = get_object_or_404(UserProfile, user=request.user)
    else:
        userprofile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('my_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/user_dashboard/my_profile.html', context)


# user change password
@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/user_dashboard/change_password.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messaage = render_to_string('accounts/password_reset_email.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                # 'phone_number' : phone_number,
                # 'uid' : user.pk,
                # 'verification_user' : verification_user,
            })
            to_mail = email
            send_male = EmailMessage(mail_subject, messaage, to=[to_mail])
            send_male.send()
            
            messages.success(request, "Password reset email has been sent to your email. Please reset your account")
            return redirect('forgotPassword')

        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotPassword')
        
    return render(request, 'accounts/forgot_password.html')



def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request, 'This link has been expired!')
        return redirect('forgotPassword')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful ')
            return redirect('signin')

        else:
            messages.error(request, 'Password does not match!')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')