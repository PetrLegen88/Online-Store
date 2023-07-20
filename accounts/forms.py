from django.forms import CharField, EmailField, IntegerField, ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from customer.models import PaymentDetail


class CustomUserCreationForm(UserCreationForm):
    first_name = CharField(max_length=30, required=True, help_text='Required, max. 30 characters.')
    last_name = CharField(max_length=30, required=True, help_text='Required, max. 30 characters.')
    email = EmailField(required=True, help_text='Required.')
    address = CharField(max_length=100, required=True, help_text='Required, street and number.')
    city = CharField(max_length=100, required=True, help_text='Required. Make sure to use correct diacritics.')
    zipcode = IntegerField(required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'city', 'zipcode', 'password1', 'password2')


class PaymentDetailForm(ModelForm):
    class Meta:
        model = PaymentDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)
        if cart:
            self.fields['cart'].widget = HiddenInput()
            self.initial['cart'] = cart
        else:
            self.fields.pop('cart')