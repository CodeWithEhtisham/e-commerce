from django.shortcuts import render
from .models import CustomUser

# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        password = request.POST['password']
        contact= request.POST['contact']
        address = request.POST['address']
        try:
            CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, contact=contact, address=address)
            return render(request, 'login.html', {'success': 'User created successfully'})
        except Exception as e:
            print(e)
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
