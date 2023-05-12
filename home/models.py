from django.db import models
from django.utils.html import mark_safe


# Create your models here.

class Banner(models.Model):
    img             =  models.ImageField(upload_to='photos/banners')
    alt_text        =  models.CharField(max_length=300)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.img.url))