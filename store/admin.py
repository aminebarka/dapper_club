from django.contrib import admin
from .models import Product, ProductAttribute, ReviewRating

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name','image_tag','sub_category', 'modified_date','is_available', 'is_featured',)
    list_editable = ('is_available', 'is_featured',)

admin.site.register(Product, ProductAdmin)




class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product','image_tag', 'color_bg', 'size','stock', 'is_available')
    list_editable = ('is_available',)


admin.site.register(ProductAttribute, ProductAttributeAdmin)

admin.site.register(ReviewRating)
