from django import template

register = template.Library()


@register.filter
def total_cart_price(cart):
    all_products = cart.products.all()
    y = 0
    for product in all_products:
        y += product.price
    return y