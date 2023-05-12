from django.urls import path
from .import views

urlpatterns = [
    path('manager_dashboard/',views.manager_dashboard,name='manager_dashboard'),
    path('user_management/',views.user_management,name='user_management'),
    path('category_management/',views.category_management,name='category_management'),
    path('add_category',views.add_category,name='add_category'),
    path('order_management/',views.order_management,name='order_management'),
    path('product_management/',views.product_management,name='product_management'),
    path('variation_management/',views.variation_management,name='variation_management'),
    path('admin_orders/', views.admin_order, name='admin_orders'),
    
    path('add_variation/', views.add_variation, name='add_variation'),
    path('update_variation/<int:variation_id>/',views.update_variation,name='update_variation'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),
    
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),
    
    path('user_block/<int:user_id>/',views.user_block,name='user_block'),
    path('user_unblock/<int:user_id>/',views.user_unblock,name='user_unblock'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
    path('update_category/<int:category_id>/', views.update_category, name="update_category"),
    path('manager_cancel_order/<int:order_number>/', views.manager_cancel_order, name='manager_cancel_order'),
    path('accept_order/<int:order_number>/', views.accept_order, name='accept_order'),
    path('complete_order/<int:order_number>/', views.complete_order, name='complete_order'),
    path('add_product/',views.add_product,name='add_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),

    #Sub category management

    path('sub_category_management/',views.sub_category_management,name='sub_category_management'),
    path('add_sub_category',views.add_sub_category,name='add_sub_category'),
    path('update_sub_category/<int:sub_cat_id>/',views.update_sub_category,name='update_sub_category'),
    path('delete_sub_category/<int:sub_cat_id>/',views.delete_sub_category,name='delete_sub_category'),
    
    # Brand Management

    path('brand_management/',views.brand_management,name='brand_management'),
    path('add_brand/',views.add_brand,name='add_brand'),
    path('update_brand/<int:brand_id>/',views.update_brand,name='update_brand'),
    path('delete_brand/<int:brand_id>/',views.delete_brand,name='delete_brand'),

    # Color Management

    path('color_management/',views.color_management,name='color_management'),
    path('add_color/',views.add_color,name='add_color'),
    path('update_color/<int:color_id>/',views.update_color,name='update_color'),
    path('delete_color/<int:color_id>/',views.delete_color,name='delete_color'),

    # Size Management

    path('size_management/',views.size_management,name='size_management'),
    path('add_size/',views.add_size,name='add_size'),
    path('update_size/<int:size_id>/',views.update_size,name='update_size'),
    path('delete_size/<int:size_id>/',views.delete_size,name='delete_size'),
    
    # price_filter Management

    path('price_filter_management/',views.price_filter_management,name='price_filter_management'),
    path('add_price_filter/',views.add_price_filter,name='add_price_filter'),
    path('update_price_filter/<int:price_filter_id>/',views.update_price_filter,name='update_price_filter'),
    path('delete_price_filter/<int:price_filter_id>/',views.delete_price_filter,name='delete_price_filter'),

    # banner Management

    path('banner_management/',views.banner_management,name='banner_management'),
    path('add_banner/',views.add_banner,name='add_banner'),
    path('update_banner/<int:banner_id>/',views.update_banner,name='update_banner'),
    path('delete_banner/<int:banner_id>/',views.delete_banner,name='delete_banner'),

    # review Management

    path('review_management/',views.review_management,name='review_management'),
    path('review_block/<int:review_id>/',views.review_block,name='review_block'),
    path('review_unblock/<int:review_id>/',views.review_unblock,name='review_unblock'),

    
    # coupon Management

    path('coupon_management/',views.coupon_management,name='coupon_management'),
    path('add_coupon/',views.add_coupon,name='add_coupon'),
    path('update_coupon/<int:coupon_id>/',views.update_coupon,name='update_coupon'),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon,name='delete_coupon'),

]
