from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Product

# @login_required
def admin_index(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, 'admin_index.html')
    else:
        return render(request, 'login.html')


def orders(request):
    return render(request, 'orders.html')

def add_product(request):
    if request.method == 'POST':
        try:
            name = request.POST['p-name']
            title = request.POST['p-title']
            quantity = request.POST['p-quantity']
            category = request.POST['p-category']
            price = request.POST['p-price']
            image = request.POST['p-image']
            types = request.POST['p-types']
            city = request.POST['p-city']
            description = request.POST['p-description']
            Product.objects.create(
                name=name,
                title=title, 
                quantity=quantity, 
                category=category, 
                price=price, 
                image=image, 
                types=types, 
                city=city, 
                description=description)
            return render(request, 'add_product.html', {'success': 'Product added successfully'})
        except Exception as e:
            print(e)
            return render(request, 'add_product.html', {'error': 'Something went wrong'})
    return render(request, 'add_product.html')

def category(request):
    return render(request, 'category.html')

def invoice(request):
    return render(request, 'invoice.html')

def view_product(request):
    return render(request, 'view_product.html')

def view_user(request):
    return render(request, 'view_user.html')

