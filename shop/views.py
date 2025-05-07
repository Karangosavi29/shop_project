from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import OrderItem, Product, Category, Brand ,Order
from .cart import Cart
from django.views.decorators.http import require_http_methods
from .forms import CheckoutForm  # we’ll create this form below



def home(request):
    """Optional: Home page with search/filter capabilities"""
    return product_list(request, template='shop/product_list.html')


def product_list(request, template='shop/product_list.html'):
    """Product listing with optional filters"""
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Filters
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('q')

    if category_id:
        products = products.filter(category_id=category_id)
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    return render(request, template, {
        'products': products,
        'categories': categories,
        'brands': brands,
    })



# views.py


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    cart.add(product=product)
    return redirect('cart_view')





def checkout_view(request):
    cart = Cart(request)
    items = cart.get_items()
    total = cart.get_total_price()

    if not items:
        return render(request, 'shop/cart_empty.html')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save Order
            order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                total=total
            )

            # Save Order Items
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                )

            cart.clear()
            return render(request, 'shop/checkout_success.html', {
                'name': form.cleaned_data.get('first_name', 'Guest')
            })
    else:
        form = CheckoutForm()

    return render(request, 'shop/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
    })




def cart_view(request):
    cart = Cart(request)
    print("CART ITEMS IN VIEW:", cart.cart)
    cart_items = cart.get_items()
    total_price = cart.get_total_price()

    if not cart_items:
        return render(request, 'shop/cart_empty.html')

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

