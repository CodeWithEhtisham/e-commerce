from django.shortcuts import render
from .models import CustomUser, Customer
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from apps.adminpanel.models import Product

from django.shortcuts import get_object_or_404, redirect
# from .models import Product
from django.conf import settings
import random
# from  import get_cart, CART_SESSION_KEY
color=None
size=None
def clear_session(request):
    request.session.flush()

def get_cart(request):
    cart = request.session.get(settings.CART_SESSION_KEY, {})
    request.session[settings.CART_SESSION_KEY] = cart
    return cart

def add_to_cart(request, product_id=None):
    global color, size
    if product_id is None:
        cart = get_cart(request)
        # print(cart)
        sub_total = sum([float(item['total_price']) for item in cart.values()])

        return render(request, 'cart.html', {'carts': cart.values(), 'sub_total': sub_total})
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    # clear_session(request)

    # Convert product_id to string for consistency
    product_id_str = str(product_id)

    # Check if the product is already in the cart
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
        cart[product_id_str]['total_price'] = str(
            int(cart[product_id_str]['quantity']) * product.price)
    else:
        cart[product_id_str] = {
            'id': product_id_str,
            'name': product.name,
            'Image': product.Image.url,
            'price': str(product.price),
            'quantity': 1,
            'total_price': str(product.price),
            'color': color,
            'size': size,

        }
        print(cart)
    cart = get_cart(request)
    # print(cart)
    sub_total = sum([float(item['total_price']) for item in cart.values()])

    return render(request, 'cart.html', {'carts': cart.values(), 'sub_total': sub_total})




# Create your views here.
def index(request):
    if request.method=="POST":
        search=request.POST['search']
        products=Product.objects.filter(name__icontains=search)
        return render(request, 'shop-grid-fullwidth.html',{
        'products':products,
        "cart_length": len(get_cart(request)),
        'carts': get_cart(request).values(),
        "sub_totals": sum([float(item['total_price']) for item in get_cart(request).values()])
        })
    products = Product.objects.all().order_by('-id')[:4]
    print("products", products)
    return render(request, 'index.html',{
        'products':products,
        "cart_length": len(get_cart(request)),
        'carts': get_cart(request).values(),
        "sub_totals": sum([float(item['total_price']) for item in get_cart(request).values()])
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
        'products':products,
        "cart_length": len(get_cart(request)),
        'carts': get_cart(request).values(),
        "sub_totals": sum([float(item['total_price']) for item in get_cart(request).values()])
    })



def checkout(request):
    cart = get_cart(request)
    sub_total = sum([float(item['total_price']) for item in cart.values()])
    return render(request, 'checkout.html',
                   {
                       "cart_length": len(get_cart(request)),
                        'carts': get_cart(request).values(),
                        "sub_total": sum([float(item['total_price']) for item in get_cart(request).values()])
                    })
from apps.adminpanel.models import Order
from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404

def checkout_success(request):
    if request.method == "POST":
        email = request.POST['email-address']
        customer, created = Customer.objects.get_or_create(email=email)

        if created:
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            contact = request.POST['phone-number']
            address = request.POST['address']
            city = request.POST['city']
            zip_code = request.POST['zip-code']
            customer.first_name = first_name
            customer.last_name = last_name
            customer.contact = contact
            customer.address = address
            customer.city = city
            customer.zip_code = zip_code
            customer.save()

        cart = get_cart(request)
        for item in cart.values():
            Order.objects.create(
                customer=customer,
                product=Product.objects.get(id=item['id']),
                quantity=item['quantity'],
                total=item['total_price'],
                order_number=random.randint(100000, 999999)
            )

        dummy = cart.copy()
        cart.clear()
        sub_total = sum([float(item['total_price']) for item in dummy.values()])
        return render(request, 'checkout-success.html', 
                      {'carts': dummy.values(), 'sub_total': sub_total})
    else:
        return render(request, 'checkout-success.html')



def collections(request):
    return render(request, 'collections.html')

def product_details(request,product_id):
    sp = Product.objects.get(id=product_id)
    # get all product except current product
    product = Product.objects.all().exclude(id=product_id).order_by('-id')
    return render(request, 'product-details.html',{
        'products':product,
        'sp':sp,
        "cart_length": len(get_cart(request)),
        'carts': get_cart(request).values(),
        "sub_totals": sum([float(item['total_price']) for item in get_cart(request).values()]),
        'color':[i.lower() for i in sp.color.split(',')],
        'size':sp.size.split(',')
        })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

from rest_framework.decorators import api_view
from django.http import JsonResponse
@api_view(['GET'])
def increament_quantity(request):
    try:
        # get product id form json
        print('request increament api',request.GET)
        product_id = request.GET.get('product_id')
        print(product_id)

        cart=get_cart(request)
        # clear_session(request)
        cart[str(product_id)]['quantity'] += 1
        cart[str(product_id)]['total_price'] = str(
            int(cart[str(product_id)]['quantity']) * float(cart[str(product_id)]['price']))
        sub_total = sum([float(cart[i]['total_price']) for i in cart])
        return JsonResponse({
            'success': True,
            'quantity': cart[str(product_id)]['quantity'],
            'total_price': cart[str(product_id)]['total_price'],
            'sub_total': sub_total,
        })
    except Exception as e:
        print(e)
        return JsonResponse({'error': f'Something went wrong {e}'})
@api_view(['GET'])
def decreament_quantity(request):
    try:
        # get product id form json
        print('request decreament api',request.GET)
        product_id = request.GET.get('product_id')
        print(product_id)

        cart=get_cart(request)
        # clear_session(request)
        if cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1
            cart[str(product_id)]['total_price'] = str(
                int(cart[str(product_id)]['quantity']) * float(cart[str(product_id)]['price']))
            sub_total = sum([float(cart[i]['total_price']) for i in cart])
            return JsonResponse({
                'success': True,
                'quantity': cart[str(product_id)]['quantity'],
                'total_price': cart[str(product_id)]['total_price'],
                'sub_total': sub_total,
            })
        else:
            # delete product from cart
            del cart[str(product_id)]
            sub_total = sum([float(cart[i]['total_price']) for i in cart])
            return JsonResponse({
                'success': True,
                'quantity': 0,
                'total_price': 0,
                'sub_total': sub_total,
            })
    except Exception as e:
        print(e)
        return JsonResponse({'error': f'Something went wrong {e}'})
    

@api_view(['GET'])
def remove_from_cart(reqeust):
    try:
        # get product id form json
        print('request remove api',reqeust.GET)
        product_id = reqeust.GET.get('product_id')
        print(product_id)
        cart=get_cart(reqeust)
        # clear_session(reqeust)
        # delete product from cart
        del cart[str(product_id)]
        sub_total = sum([float(cart[i]['total_price']) for i in cart])
        return JsonResponse({
            'success': True,
            'quantity': 0,
            'total_price': 0,
            'sub_total': sub_total,
        })
    except Exception as e:
        print(e)
        return JsonResponse({'error': f'Something went wrong {e}'})
    
@api_view(['GET'])
def change_color(request):
    try:
        # get product id form json
        global color
        print('request change color api',request.GET)
        product_id = request.GET.get('id')
        print(product_id)
        c = request.GET.get('color')
        print(c)
        color=c
        
        return JsonResponse({
            'success': True})
    except Exception as e:
        return JsonResponse({'error': f'Something went wrong {e}'})
    
@api_view(['GET'])
def change_size(request):
    try:
        # get product id form json
        global size
        print('request change size api',request.GET)
        product_id = request.GET.get('id')
        print(product_id)
        size_type = request.GET.get('size')
        print(size_type)
        size=size_type
        return JsonResponse({
            'success': True})
    except Exception as e:
        print(e)
        return JsonResponse({'error': f'Something went wrong {e}'})
        