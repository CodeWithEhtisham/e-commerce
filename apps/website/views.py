from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    return render(request, 'index.html')


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
    return render(request, 'shop_grid_fullwidth.html')


def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def checkout_success(request):
    return render(request, 'checkout-success.html')

def collections(request):
    return render(request, 'collections.html')

def product_details(request):
    return render(request, 'product-details.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))