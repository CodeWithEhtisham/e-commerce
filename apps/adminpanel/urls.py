
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', views.admin_index, name='admin_index'),
    path('admin/orders', views.orders, name='orders'),
    path('admin/add_product', views.add_product, name='add_product'),
    path('admin/category', views.category, name='category'),
    path('admin/invoice', views.invoice, name='invoice'),
    path('admin/view_product', views.view_product, name='view_product'),
    path('admin/view_user', views.view_user, name='view_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)