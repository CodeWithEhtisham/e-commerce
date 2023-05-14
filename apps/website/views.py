from django.shortcuts import render
from .models import CustomUser, AddToCart
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from apps.adminpanel.models import Product

from django.shortcuts import get_object_or_404, redirect
# from .models import Product
from django.conf import settings
# from  import get_cart, CART_SESSION_KEY

def get_cart(request):
    cart = request.session.get(settings.CART_SESSION_KEY, [])
    request.session[settings.CART_SESSION_KEY] = cart
    return cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    # Add the product to the session cart
    cart.append(product.id)

    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart)

    return render(request, 'cart.html', {'carts': products})

# Create your views here.
def index(request):
    if request.method=="POST":
        pass
    products = Product.objects.all().order_by('-id')[:4]
    for i in products:
        print(i.name)
    return render(request, 'index.html',{
        'products':products
        })


def login_user(request):
    if not CustomUser.objects.filter(
        email='admin@test.com').exists():
        CustomUser.objects.create_superuser(
            username='admin',
            first_name='admin',
            last_name='admin',
            email='admin@test.com',
            password='admin')
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                auth=authenticate(request, username=user.username, password=password)
                login(request, auth)
                if user.is_superuser:
                    print('admin')
                    return HttpResponseRedirect(reverse("admin_index"))
                else:
                    print('sales man')
                    return HttpResponseRedirect(reverse("admin_index"))
            else:

                return render(request, 'login.html', {'error': 'Invalid password'})
        except Exception as e:
            print(e)
            return render(request, 'login.html', {'error': 'Invalid email'})
    return render(request, 'login.html')

def register(request):
    print(request.method)
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        password = request.POST['password']
        contact= request.POST['contact']
        address = request.POST['address']
        # print(first_name, last_name, email, password, contact, address)
        try:
            CustomUser.objects.create_user(username=first_name,first_name=first_name, last_name=last_name, email=email, password=password, contact=contact, address=address)
            return render(request, 'login.html', {'success': 'User created successfully'})
        except Exception as e:
            print('error',e)
            return render(request, 'register.html', {'error': 'Something went wrong'})

    return render(request, 'register.html')


def shop_grid_fullwidth(request):
    products=Product.objects.all().order_by('-id')
    return render(request, 'shop-grid-fullwidth.html',{
        'products':products
    })

from django.db.models import Sum
def carts(request):
    # if product_id:
    #     product = Product.objects.get(id=product_id)
    #     if AddToCart.objects.filter(product=product, user=request.user).exists():
    #         cart = AddToCart.objects.get(product=product, user=request.user)
    #         cart.quantity = cart.quantity + 1
    #         cart.total_price = cart.quantity * product.price
    #         cart.save()
    #     else:
    #         cart = AddToCart.objects.create(product=product, user=request.user)
    #         cart.quantity = 1
    #         cart.total_price = product.price
    #         cart.save()
    # carts = AddToCart.objects.filter(user=request.user).select_related('product').order_by('-id')
    # sub_total = carts.aggregate(Sum('total_price'))['total_price__sum']
    # return render(request, 'cart.html',{    
    #     'carts':carts,
    #     'sub_total':sub_total
    #     })

    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart)

    return render(request, 'cart.html', {'products': products})


def checkout(request):
    return render(request, 'checkout.html')

def checkout_success(request):
    return render(request, 'checkout-success.html')

def collections(request):
    return render(request, 'collections.html')

def product_details(request,product_id):
    sp = Product.objects.get(id=product_id)
    # get all product except current product
    product = Product.objects.all().exclude(id=product_id).order_by('-id')
    return render(request, 'product-details.html',{
        'products':product,
        'sp':sp
        })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))