from django.core.validators import MinValueValidator
from django.db.models import *
from online_store.settings import ProductType, PaymentMethods
from accounts.models import CustomUser, User


class MainCategory(Model):
    name = CharField(max_length=32, null=False, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SecondaryCategory(Model):
    name = CharField(max_length=32, null=False, unique=True)
    category = ForeignKey(MainCategory, on_delete=CASCADE, related_name='secondary_categories')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Producer(Model):
    name = CharField(max_length=16, null=False)

    def __str__(self):
        return self.name


class Product(Model):
    title = CharField(max_length=64)
    description = TextField()
    price = FloatField()
    category = ForeignKey(SecondaryCategory, related_name='second_category', on_delete=CASCADE)
    product_type = CharField(max_length=32, choices=ProductType.choices(), default=ProductType.CLASSIC)
    thumbnail = ImageField(upload_to='photos')
    producer = ForeignKey(Producer, null=True, related_name='producer', on_delete=CASCADE)
    availability = IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "(available " + str(self.availability) + ") " + str(self.title)


class Cart(Model):
    user = ForeignKey(User, on_delete=CASCADE, default=1)
    paid = BooleanField(default=False, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    total = DecimalField(default=0, max_digits=10, decimal_places=2)
    bought_items = TextField()

    def __str__(self):
        if self.paid:
            payment = "paid"
        else:
            payment = "need payment"
        return f"Cart of {self.user} ({self.id}) ({payment})"


class Item(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"(Order num: {self.cart.id}) {self.product.title} ({self.quantity})"


class PaymentDetail(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, default=None, null=True)
    method = CharField(max_length=32, choices=PaymentMethods.choices(), default=PaymentMethods.CreditCard)
    address = TextField()
    city = CharField(max_length=100)
    zipcode = IntegerField()

    def __str__(self):
        return f"Payment Detail of order: {self.cart.id} ({self.cart.user})"

