from django.urls import path
from . import views
from . import otp_verification as o

urlpatterns = [

    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name='signout'),

    path('activate/<uidb64>/<token>/', views.activate_email , name='activate'),
    path('mobile_otp/', o.mobile_otp, name='mobile_otp'),
    path('resent-otp/', o.resent_otp, name='resent_otp'),
    path('validate_otp/<phone_number>/<uid>/<verification_user>/', o.otp_activation , name='validate_otp'),


    # user dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_order/', views.my_order, name='my_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my_profile/', views.my_profile, name='my_profile'),    
    # path('my_address/', views.my_address, name='my_address'),
    # path('my_coupon/', views.my_coupon, name='my_coupon'),
    path('change_password/', views.change_password, name='change_password'),




    path('forgotPassword/', views.forgot_password, name='forgotPassword'),
    path('resetPassword/', views.reset_password, name='resetPassword'),


    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),


# <phone_number>/<uid>/<verification_user>/
]
