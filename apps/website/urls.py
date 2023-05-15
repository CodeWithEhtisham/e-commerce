
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns     
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('shop_grid_fullwidth', views.shop_grid_fullwidth, name='shop_grid_fullwidth'),
    path('cart/<int:product_id>/', views.add_to_cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('checkout_success', views.checkout_success, name='checkout_success'),
    path('collections', views.collections, name='collections'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('logout', views.logout_user, name='logout'),

    path('api/increament_quantity/', views.increament_quantity, name='increament_quantity'),
    path('api/decreament_quantity/', views.decreament_quantity, name='decreament_quantity'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# # Serving the media files in development mode
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += staticfiles_urlpatterns()