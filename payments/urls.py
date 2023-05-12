from django.urls import path
from . import views

urlpatterns = [
    path('order-payment', views.order_payment, name='order_payment'),
    path('order-complete', views.order_complete, name='order-complete'),
    

]