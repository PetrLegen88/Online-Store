from django import forms
from customer.models import Product, SecondaryCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = SecondaryCategory
        fields = "__all__"


