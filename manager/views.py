from django.shortcuts import render,redirect
from accounts.models import Account
from store.models import Product, ProductAttribute, ReviewRating
from orders.models import Order
from carts.models import Coupon
from category.models import Category, SubCategory, Size, Color, PriceFilter, Brand
from home.models import Banner
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from .forms import ProductForm, ProductAttributeForm, SubCategoryForm, CategoryForm, BrandForm, ColorForm, SizeForm, PriceFilterForm, BannerForm, CouponForm





# Create your views here.

@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def manager_dashboard(request):
    if request.user.is_superadmin:

        user_count = Account.objects.filter(is_superadmin=False).count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.filter(is_ordered=True).count()
        category_count = Category.objects.all().count()
        variation_count = ProductAttribute.objects.all().count()
        admin_order_count = Order.objects.filter(user__is_superadmin=True).count()
        

        context = {
            'user_count': user_count,
            'product_count': product_count,
            'order_count' : order_count,
            'category_count' : category_count,
            'variation_count' : variation_count,
            'admin_order_count' : admin_order_count
        }

        return render(request,'manager/manager_dashboard.html',context)
    else:
        return redirect('index')


# Manage users
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def user_management(request):
    if request.method == "POST":
      key = request.POST['key']
      users = Account.objects.filter( Q(first_name__icontains=key) | Q(last_name__icontains=key) | Q(username__startswith=key) | Q(email__icontains=key), is_superadmin = False).order_by('-id')
    else:
        users = Account.objects.filter(is_superadmin=False).order_by('-id')

    paginator = Paginator(users,10)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
        'users' : paged_users
    }
    return render(request, 'manager/user_management.html',context)



@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def user_block(request, user_id):
  user = Account.objects.get(id=user_id)
  user.is_active = False
  user.save()
  return redirect('user_management')



@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def user_unblock(request, user_id):
  user = Account.objects.get(id=user_id)
  user.is_active= True
  user.save()
  return redirect('user_management')


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def category_management(request):
    categories = Category.objects.all().order_by('-id')

    context = {
        'categories' :categories
    }

    return render(request, 'manager/category_management.html',context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('category_management')

    else:
      messages.error(request, "Catergory with this same name already exists")
      return redirect('add_category')
  else:
    form = CategoryForm()
    context = {
      'form': form
    }
  return render(request, 'manager/add_category.html', context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_category(request, category_id):
  category = Category.objects.get(id=category_id)
  category.delete()
  return redirect('category_management')


# Update Category
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_category(request, category_id):
  category = Category.objects.get(id=category_id)
  form = CategoryForm(instance=category)
  
  if request.method == 'POST':
    try:
      form = CategoryForm(request.POST, instance=category)
      if form.is_valid():
        form.save()
        return redirect('category_management')
    
    except Exception as e:
      raise e

  context = {
    'category': category,
    'form': form
  }
  return render(request, 'manager/update_category.html', context)


# Sub category management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def sub_category_management(request):
    sub_categories = SubCategory.objects.all().order_by('-id')

    context = {
        'sub_categories' :sub_categories
    }

    return render(request, 'manager/sub_category_management .html',context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_sub_category(request):
  if request.method == 'POST':
    form = SubCategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('sub_category_management')
  else:
    form = SubCategoryForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_sub_category.html', context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_sub_category(request, sub_cat_id):
  sub_category = SubCategory.objects.get(id = sub_cat_id)
  form = SubCategoryForm(instance = sub_category)
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, instance = sub_category)
    form.save()

    return redirect('sub_category_management')

  context = {
    'form' : form
  }
  return render(request, 'manager/update_sub_category.html', context)



@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_sub_category(request, sub_cat_id):
  sub_category = SubCategory.objects.get(id=sub_cat_id)
  sub_category.delete()
  return redirect('sub_category_management')


#brand management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def brand_management(request):
  brands = Brand.objects.all().order_by('-id')
  context = {
    'brands': brands
  }
  return render(request, 'manager/brand_management.html', context)


#add brand
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_brand(request):
  if request.method == 'POST':
    form = BrandForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('brand_management')

    else:
      print(form.errors)

  else:
    form = BrandForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_brand.html', context)


# Update brand
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_brand(request, brand_id):
  brand = Brand.objects.get(id = brand_id)
  form = BrandForm(instance = brand)
  if request.method == 'POST':
    form = BrandForm(request.POST, request.FILES, instance = brand)
    if form.is_valid():
      form.save()
      return redirect('brand_management')
  context = {
    'form':form
  }
  return render(request, 'manager/add_brand.html', context)


#delete brand
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_brand(request, brand_id):
  brand = Brand.objects.get(id = brand_id)
  brand.delete()
  return redirect('brand_management')


# Color management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def color_management(request):
  colors = Color.objects.all().order_by('-id')
  context = {
    'colors': colors
  }
  return render(request, 'manager/color_management.html', context)


#add Color
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_color(request):
  if request.method == 'POST':
    form = ColorForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('color_management')

    else:
      print(form.errors)

  else:
    form = ColorForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_color.html', context)


# Update color
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_color(request, color_id):
  color =  Color.objects.get(id = color_id)
  form = ColorForm(instance = color)
  if request.method == 'POST':
    form = ColorForm(request.POST, instance = color)
    if form.is_valid():
      form.save()
      return redirect('color_management')
  context = {
    'form':form
  }
  return render(request, 'manager/add_color.html', context)


#delete color
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_color(request, color_id):
  color = Color.objects.get(id = color_id)
  color.delete()
  return redirect('color_management')



# Size management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def size_management(request):
  sizes = Size.objects.all().order_by('-id')
  context = {
    'sizes': sizes
  }
  return render(request, 'manager/size_management.html', context)


#add size
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_size(request):
  if request.method == 'POST':
    form = SizeForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('size_management')

    else:
      print(form.errors)

  else:
    form = SizeForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_size.html', context)


# Update size
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_size(request, size_id):
  size =  Size.objects.get(id = size_id)
  form = SizeForm(instance = size)
  if request.method == 'POST':
    form = SizeForm(request.POST, instance = size)
    if form.is_valid():
      form.save()
      return redirect('size_management')
  context = {
    'form':form
  }
  return render(request, 'manager/add_size.html', context)


#delete size
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_size(request,size_id):
  print('hai')
  size = Size.objects.get(id = size_id)
  size.delete()
  return redirect('size_management')




# Price-filter management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def price_filter_management(request):
  prices = PriceFilter.objects.all().order_by('id')
  context = {
    'prices': prices
  }
  return render(request, 'manager/price_filter_management.html', context)


#add Price-filter
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_price_filter(request):
  if request.method == 'POST':
    form = PriceFilterForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('price_filter_management')

    else:
      print(form.errors)

  else:
    form = PriceFilterForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_price_filter.html', context)


# Update Price-filter
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_price_filter(request, price_filter_id):
  price_filter =  PriceFilter.objects.get(id = price_filter_id)
  form = PriceFilterForm(instance = price_filter)
  if request.method == 'POST':
    form = PriceFilterForm(request.POST, instance = price_filter)
    if form.is_valid():
      form.save()
      return redirect('price_filter_management')
  context = {
    'form':form
  }
  return render(request, 'manager/add_price_filter.html', context)


#delete Price-filter
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_price_filter(request, price_filter_id):
  print('hai')
  price_filter = PriceFilter.objects.get(id = price_filter_id)
  price_filter.delete()
  return redirect('price_filter_management')



# banner management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def banner_management(request):
  banners = Banner.objects.all().order_by('-id')
  context = {
    'banners': banners
  }
  return render(request, 'manager/banner_management.html', context)


#add banner
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_banner(request):
  if request.method == 'POST':
    form = BannerForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('banner_management')

    else:
      print(form.errors)

  else:
    form = BannerForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_banner.html', context)


# Update banner
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_banner(request, banner_id):
  banner =  Banner.objects.get(id = banner_id)
  form = BannerForm(instance = banner)
  if request.method == 'POST':
    form = BannerForm(request.POST, request.FILES, instance = banner)
    if form.is_valid():
      form.save()
      return redirect('banner_management')
  context = {
    'form':form
  }
  return render(request, 'manager/add_banner.html', context)


#delete Banner
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_banner(request, banner_id):
  banner = Banner.objects.get(id = banner_id)
  banner.delete()
  return redirect('banner_management')


# Review management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def review_management(request):
  reviews = ReviewRating.objects.all().order_by('-id')
  context = {
    'reviews': reviews
  }
  return render(request, 'manager/review_management.html', context)


#block review
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def review_block(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status = False
  review.save()
  return redirect('review_management')

# unblock review
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def review_unblock(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status= True
  review.save()
  return redirect('review_management')



# coupon management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def coupon_management(request):
  coupons = Coupon.objects.all().order_by('-id')
  context = {
    'coupons': coupons
  }
  return render(request, 'manager/coupon_management.html', context)


#add coupon
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_coupon(request):
  if request.method == 'POST':
    form = CouponForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('coupon_management')

    else:
      print(form.errors)

  else:
    form = CouponForm()

  context = {
    'form': form
  }
  return render(request, 'manager/add_coupon.html', context)


# Update coupon
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_coupon(request, coupon_id):
  coupon =  Coupon.objects.get(id = coupon_id)
  form = CouponForm(instance = coupon)
  if request.method == 'POST':
    form = CouponForm(request.POST, instance = coupon)
    if form.is_valid():
      form.save()
      return redirect('coupon_management')
  context = {
    'form':form
  }
  return render(request, 'manager/add_coupon.html', context)


#delete coupon
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_coupon(request, coupon_id):
  coupon = Coupon.objects.get(id = coupon_id)
  coupon.delete()
  return redirect('coupon_management')



#Manage product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def product_management(request):
  if request.method == "POST":
    key = request.POST['key']
    products = Product.objects.filter(Q(product_name__icontains=key) | Q(slug__startswith=key) | Q(sub_category__category__category_name__startswith=key)).order_by('-id')
  else:
    products = Product.objects.all().order_by('-id')

  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)
  
  context = {
    'products': paged_products
  }
  return render(request, 'manager/product_management.html', context)


# Add Product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_product(request):
  if request.method == 'POST':
    print("hoi")
    form = ProductForm(request.POST, request.FILES)
    print("pooi")
    if form.is_valid():
      print("hai")
      form.save()
      return redirect('product_management')
    else:
      print(form.errors)
  else:
    form = ProductForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_product.html', context)



    
# Edit Product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def edit_product(request, product_id):
  product = Product.objects.get(id=product_id)
  form = ProductForm(instance=product)
  
  if request.method == 'POST':
    try:
      form = ProductForm(request.POST, request.FILES, instance=product)
      if form.is_valid():
        form.save()
        
        return redirect('product_management')
    
    except Exception as e:
      raise e

  context = {
    'product': product,
    'form': form
  }
  return render(request, 'manager/edit_product.html', context)


# Delete Product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_product(request, product_id):
  product = Product.objects.get(id=product_id)
  product.delete()
  return redirect('product_management')




  # Manage Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def order_management(request):
  if request.method =="POST":
    key = request.POST['key']
    orders = Order.objects.filter(Q(is_ordered=True), Q(order_number__icontains=key) | Q(user__email__icontains=key) | Q(first_name__startswith=key)).order_by('-id')
  else:
    orders = Order.objects.filter(is_ordered=True).order_by('-id')
    

  context = {
    'orders': orders
  }
  return render(request, 'manager/order_management.html', context)


# Accept Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def accept_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Shipped'
  order.save()
  
  return redirect('order_management')




# Complete Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def complete_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Delivered'
  order.save()
  
  return redirect('order_management')



# Cancel Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def manager_cancel_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Cancelled'
  order.save()

  if request.user.is_admin:
    return redirect('admin_orders')

  else:
    return redirect('order_management')


  # Manage Variation
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def variation_management(request):
  if request.method == 'POST':
    keyword = request.POST['keyword']
    variations = ProductAttribute.objects.filter(Q(product__product_name__icontains=keyword) | Q(product__sub_category__category__category_name__startswith=keyword) | Q(color__color_name__startswith=keyword | Q(size__size__startswith=keyword)).order_by('-id'))
  
  else:
    variations = ProductAttribute.objects.all().order_by('-id')
  
  paginator = Paginator(variations, 10)
  page = request.GET.get('page')
  paged_variations = paginator.get_page(page)
  
  context = {
    'variations': paged_variations
  }
  return render(request, 'manager/variation_management.html', context)


# Add Variation
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_variation(request):
  
  if request.method == 'POST':
    form = ProductAttributeForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('variation_management')
  
  else:
    form = ProductAttributeForm()
  
  context = {
    'form': form
  }
  return render(request, 'manager/add_variation.html', context)



# update variation 
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_variation(request, variation_id):
  variation = ProductAttribute.objects.get(id = variation_id)
  if request.method == 'POST':
    form = ProductAttributeForm(request.POST, instance = variation)
    if form.is_valid():
      form.save()
      return redirect('variation_management')
  else:
    form = ProductAttributeForm(instance = variation)

  context = {
    'form':form,
    'variation':variation
  }

  return render(request, 'manager/update_variation.html', context)


# delete variation 
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_variation(request, variation_id):
  variation = ProductAttribute.objects.get(id = variation_id)
  variation.delete()
  return redirect('variation_management')


    
# Admin orders
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def admin_order(request):
  current_user = request.user
  if request.method == 'POST':
    keyword = request.POST['keyword']
    orders = Order.objects.filter(Q(user=current_user), Q(is_ordered=True), Q(order_number__contains=keyword) | Q(user__email__icontains=keyword) | Q(first_name__startswith=keyword) | Q(last_name__startswith=keyword) | Q(phone__startswith=keyword)).order_by('-created_at')
    
  else:
    orders = Order.objects.filter(user=current_user, is_ordered=True).order_by('-created_at')
  
  paginator = Paginator(orders, 10)
  page = request.GET.get('page')
  paged_orders = paginator.get_page(page)
  context = {
    'orders': paged_orders,
  }
  return render(request, 'manager/admin_orders.html', context)


# admin password change
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def admin_change_password(request):
  if request.method == 'POST':
    current_user = request.user
    current_password = request.POST['current_password']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    if password == confirm_password:
      if check_password(current_password, current_user.password):
        if check_password(password, current_user.password):
          messages.warning(request, 'Current password and new password is same')
        else:
          hashed_password = make_password(password)
          current_user.password = hashed_password
          current_user.save()
          messages.success(request, 'Password changed successfully')
      else:
        messages.error(request, 'Wrong password')
    else:
      messages.error(request, 'Passwords does not match')
  
  return render(request, 'manager/admin_password.html')