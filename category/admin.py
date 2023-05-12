from django.contrib import admin
from .models import Category, Brand, SubCategory, Size, Color, PriceFilter

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display = ('category_name','slug')

admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display=('name', 'image_tag')
admin.site.register(Brand,BrandAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category', 'category')
admin.site.register(SubCategory, SubCategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display=('id','name', 'color_bg')
admin.site.register(Color, ColorAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display=('id', 'size')
admin.site.register(Size)


class PriceFilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')
admin.site.register(PriceFilter, PriceFilterAdmin)