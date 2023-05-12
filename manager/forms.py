from django import forms
from store.models import Product, ProductAttribute
from category.models import Category, SubCategory, Color, Size, PriceFilter, Brand
from home.models import Banner
from carts.models import Coupon

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'image1', 'image2', 'image3', 'image4', 'sub_category', 'brand', 'price_filter', 'is_available', 'is_featured']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'
        self.fields['is_featured'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'

class ProductAttributeForm(forms.ModelForm):

    class Meta:
        model = ProductAttribute
        fields = ['product', 'color', 'size', 'stock', 'is_available']

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'



class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['category', 'sub_category']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ColorForm(forms.ModelForm):

    class Meta:
        model = Color
        fields = ['name', 'color_code']

    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class SizeForm(forms.ModelForm):

    class Meta:
        model = Size
        fields = ['size']

    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PriceFilterForm(forms.ModelForm):

    class Meta:
        model = PriceFilter
        fields = ['price']

    def __init__(self, *args, **kwargs):
        super(PriceFilterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    
class BannerForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['img', 'alt_text']

    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class DateInput(forms.DateTimeInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    
    expiry_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Coupon
        fields = ['coupon_code','discount_price', 'minimum_amount', 'expiry_date', 'is_active']

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_active'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'






    