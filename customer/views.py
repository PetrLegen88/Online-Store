from django.contrib import messages
import requests
from django.core.paginator import Paginator
from django.shortcuts import *
from django.db.models import Q
from customer.models import *
from customer.forms import ProductForm, CategoryForm
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from accounts.forms import PaymentDetailForm
from customer.models import PaymentDetail
from django.contrib.admin.views.decorators import staff_member_required


def base_context(request):
    categories = SecondaryCategory.objects.all()
    if request.user.is_authenticated:
        user = request.user.customuser
        city = user.city
        weather_data = get_current_weather(city)
        if weather_data is not None:
            temperature, weather_description, icon_url = weather_data
            return {
                'user': user,
                'temperature': temperature,
                'weather_description': weather_description,
                'icon_url': icon_url,
                'categories': categories,
            }
        else:
            return {'Unknown city': city, 'categories': categories}
    else:
        return {'categories': categories}


def homepage(request):
    products = Product.objects.all().order_by('price')
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = SecondaryCategory.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    context.update(base_context(request))
    return render(request, 'homepage.html', context)


def get_current_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=6bcbc258ca1449deb93c6851e10afeff'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temperature = round(data['main']['temp'] - 273.15, 1) # convert from kelvin to celsius
        weather_description = data['weather'][0]['description']
        icon_id = data['weather'][0]['icon']
        icon_url = f'http://openweathermap.org/img/wn/{icon_id}.png'
        return temperature, weather_description, icon_url
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except KeyError as e:
        print(f"Error: Invalid response received from server: {e}")
        return None
    except IndexError as e:
        print(f"Error: No weather data found for {city}.")
        return None


@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ProductForm()
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'new_product.html', context)


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'new_category.html', context)


@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product_id': product_id
    }
    context.update(base_context(request))
    return render(request, 'edit_product.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    context.update(base_context(request))
    return render(request, 'product_detail.html', context)


def contact(request):
    context = {}
    context.update(base_context(request))
    return render(request, 'contact.html', context)


def search(request):
    search = request.POST.get('search')
    categories = SecondaryCategory.objects.all()
    context = {
        'search': search,
        'categories': categories,
    }
    if request.method == "POST":
        if search:
            products = Product.objects.filter(title__contains=search)
            sorted_products = sorted(products, key=lambda p: p.title)
            context['sorted_products'] = sorted_products
            if products:
                context.update(base_context(request))
                return render(request, 'search.html', context)
            else:
                messages.error(request, 'No products found for your search.')
        else:
            messages.error(request, 'Invalid input')
    context.update(base_context(request))
    return render(request, 'search.html', context)


def filter_by_main_category(request, main_category_name):
    main_category = get_object_or_404(MainCategory, name=main_category_name)
    products = Product.objects.filter(category__category=main_category)
    categories = SecondaryCategory.objects.all()
    context = {
        'main_category': main_category,
        'products': products,
        'categories': categories,
    }
    context.update(base_context(request))
    return render(request, 'filter_by_main_category.html', context)


@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user, paid=False).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
    total = 0
    items = Item.objects.filter(cart=cart)
    for item in items:
        total += item.product.price * item.quantity
    total = round(total, 2)
    context = {
        'cart': cart,
        'total': total,
        'items': items,
    }
    context.update(base_context(request))
    return render(request, 'view_cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        if product.availability >= quantity:
            product.availability -= quantity
            product.save()
            cart = Cart.objects.filter(user=request.user, paid=False).first()
            if cart is None:
                cart = Cart.objects.create(user=request.user)
            item = Item.objects.filter(product=product, cart=cart).first()
            if item is None:
                Item.objects.create(product=product, quantity=quantity, cart=cart)
            else:
                item.quantity += quantity
                item.save()
    return redirect('view_cart')


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user=request.user, paid=False).first()
    item = Item.objects.get(cart=cart, product=product)
    product.availability += item.quantity
    item.quantity = 0
    product.save()
    item.save()
    item.delete()
    return redirect('view_cart')


@login_required
def order_confirm(request):
    user = CustomUser.objects.get(id=request.user.id)
    cart = Cart.objects.filter(user=request.user, paid=False).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
    product_totals = []
    total = 0
    items = Item.objects.filter(cart=cart)
    for item in items:
        product_total = round(item.product.price * item.quantity, 2)
        product_totals.append({'product': item.product, 'total': product_total, 'quantity': item.quantity})
        total += product_total
        print(product_totals)
    total = round(total, 2)
    cart.total = total
    cart.save()
    context = {
        'cart': cart,
        'product_totals': product_totals,
        'total': total,
        'user': user,
    }
    context.update(base_context(request))
    return render(request, 'order_confirm.html', context)


def filter_products(request, category_name=None, min_price=None, max_price=None):
    filter_q = Q()

    if min_price is not None:
        filter_q &= Q(price__gte=min_price)

    if max_price is not None:
        filter_q &= Q(price__lte=max_price)

    if category_name is not None:
        category = get_object_or_404(SecondaryCategory, name=category_name)
        filter_q &= Q(category=category)

    products_created_at = Product.objects.all().order_by('-created_at')
    categories = SecondaryCategory.objects.all()
    products = Product.objects.filter(filter_q).order_by('price')

    context = {
        'products_created_at': products_created_at,
        'category_name': category_name,
        'min_price': min_price,
        'max_price': max_price,
        'categories': categories,
        'products': products,
    }
    context.update(base_context(request))
    return render(request, 'filter_products.html', context)


@login_required
def delivery_payment(request):
    cart = Cart.objects.filter(user=request.user, paid=False).first()
    if request.method == 'POST':
        form = PaymentDetailForm(request.POST, request.FILES)
        if form.is_valid():
            payment_detail = PaymentDetail.objects.create(
                cart=cart,
                method=form.cleaned_data["method"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                zipcode=form.cleaned_data["zipcode"]
            )
            deleted_items = list(cart.item_set.all().values_list('product__title', 'quantity'))
            formatted_deleted_items = [item[0] + " (" + str(item[1]) + ") " for item in deleted_items]
            cart.bought_items = formatted_deleted_items
            cart.item_set.all().delete()
            cart.paid = True
            cart.save()
            return redirect('payment_success', cart_id=cart.id)
    else:
        form = PaymentDetailForm()
    context = {
        'form': form,
        'errors': form.errors
    }
    context.update(base_context(request))
    return render(request, 'delivery_payment.html', context)


def payment_success(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart
    }
    context.update(base_context(request))
    return render(request, 'payment_success.html', context)
