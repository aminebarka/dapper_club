from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid', 'status')
admin.site.register(Payment, PaymentAdmin)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number', 'full_name','full_address', 'status')
admin.site.register(Order, OrderAdmin)



class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'order', 'quantity', 'product_price')
admin.site.register(OrderProduct, OrderProductAdmin)
