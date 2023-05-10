
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('shop_grid_fullwidth', views.shop_grid_fullwidth, name='shop_grid_fullwidth'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('checkout_success', views.checkout_success, name='checkout_success'),
    path('collections', views.collections, name='collections'),
    path('product_details', views.product_details, name='product_details'),
]