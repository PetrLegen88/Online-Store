"""online_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from customer.views import *
from accounts.views import signup, logout_view

urlpatterns = [
  path('', homepage, name='homepage'),
  path('admin/', admin.site.urls),
  path('accounts/logout/', logout_view),
  path('accounts/', include('django.contrib.auth.urls')),
  path('signup/', signup, name='signup'),
  path('new_product/', add_product, name='new_product'),
  path('new_category/', add_category, name='new_category'),
  path('products/<int:product_id>/edit/', edit_product, name='edit_product'),
  path('product_detail/<int:product_id>/', product_detail, name='product_detail'),

  path('main_category/<str:main_category_name>/', filter_by_main_category, name='filter_by_main_category'),
  path('categories/<str:category_name>/', filter_products, name='filter_by_secondary_category'),
  path('categories/<str:category_name>/price/max/<int:max_price>/', filter_products, name='filter_products'),
  path('categories/<str:category_name>/price/min/<int:min_price>/', filter_products, name='filter_products'),
  path('categories/<str:category_name>/price/range/<int:min_price>/<int:max_price>/', filter_products, name='filter_products'),
  path('price/min/<int:min_price>/', filter_products, name='product_list_min_price'),
  path('price/max/<int:max_price>/', filter_products, name='product_list_max_price'),
  path('price/range/<int:min_price>/<int:max_price>/', filter_products, name='product_list_price_range'),

  path('contact', contact, name='contact'),
  path('search', search, name='search'),
  path('accounts/profile/', homepage),
  path('view_cart/', view_cart, name='view_cart'),
  path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
  path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
  path('order_confirm/', order_confirm, name='order_confirm'),

  path('delivery_payment/', delivery_payment, name='delivery_payment'),
  path('payment/success/<int:cart_id>/', payment_success, name='payment_success'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
