from django.urls import path
from . import views

urlpatterns = [
      path('',views.cart, name="cart"),
      path('add-to-cart',views.add_to_cart, name="add_to_cart"),
      path('delete-from-cart/<int:prod_id>/',views.cart_delete, name="cart_delete"),
      path('update-cart',views.cart_update, name="cart_update"),

      path('wishlist/add-to-wishlist',views.add_to_wishlist, name="add_to_wishlist"),
      path('delete-from-wishlist',views.delete_from_wishlist, name="delete_from_wishlist"),
      path('wishlist/',views.wishlist, name="wishlist"),

      path('apply-coupon', views.apply_coupon, name="apply_coupon")







]