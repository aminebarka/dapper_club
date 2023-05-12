from django.contrib import admin
from .models import Banner

# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    list_display =('id', 'image_tag')

admin.site.register(Banner, BannerAdmin)

