from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Product
import os
from apps.website.models import CustomUser
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
            # Retrieve form data
            name = request.POST['p-name']
            title = request.POST['p-title']
            quantity = request.POST['p-quantity']
            category = request.POST['p-category']
            price = request.POST['p-price']
            image = request.FILES['p-image']
            types = request.POST['p-type']
            city = request.POST['p-city']
            description = request.POST['p-description']

            # Save image in media folder
            image_name = image.name
            if not os.path.exists('media'):
                os.mkdir('media')
            if not os.path.exists('media/product_images'):
                os.mkdir('media/product_images')
            image_path = os.path.join('product_images/', image_name)
            with open(os.path.join('media/', image_path), 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Store image path in the database
            Product.objects.create(
                user=request.user,
                name=name,
                title=title, 
                quantity=quantity, 
                category=category, 
                price=price, 
                Image=image_path,  # Store the image path instead of the image itself
                types=types, 
                city=city, 
                description=description)
            return render(request, 'add_product.html', {'success': 'Product added successfully'})
        except Exception as e:
            print('error',e)
            return render(request, 'add_product.html', {'error': 'Something went wrong'})
    return render(request, 'add_product.html')

def category(request):
    return render(request, 'category.html')

def invoice(request):
    return render(request, 'invoice.html')

def view_product(request):
    if request.method=="POST":
        pass
    if request.user.is_superuser:
        product=Product.objects.all()
    else:
        product=Product.objects.filter(user=request.user)
    return render(request, 'view_product.html',{'product':product})

from django.db.models import Sum,Count
def view_user(request):
    if request.method=="POST":
        pass
    # get all user not admin
    user = CustomUser.objects.filter(is_superuser=False).annotate(
    sum_quantity=Sum('product__quantity'),
    num_products=Count('product')
)
    return render(request, 'view_users.html',{'user':user})

