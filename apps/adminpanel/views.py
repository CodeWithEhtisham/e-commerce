from django.shortcuts import render

# Create your views here.
def admin_index(request):
    return render(request, 'admin_index.html')

def orders(request):
    return render(request, 'orders.html')

def add_product(request):
    return render(request, 'add_product.html')

def category(request):
    return render(request, 'category.html')

def invoice(request):
    return render(request, 'invoice.html')

def view_product(request):
    return render(request, 'view_product.html')

def view_user(request):
    return render(request, 'view_user.html')

