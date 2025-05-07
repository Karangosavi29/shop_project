# shop/urls.py

from django.urls import  path

from django.contrib import admin  # ✅ Correct admin

from . import views

app_name = 'shop'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', views.product_list, name='product_list'),  # ✅ for second issue
    path('cart/', views.cart_view, name='cart_view'), # ✅ this line fixes the error
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    
    # Optional: Home route if needed
    path('home/', views.home, name='home'),
    
    

]