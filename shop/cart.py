# shop/cart.py

from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
        print("🛒 SAVED CART:", self.cart)

    def get_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        for product in products:
            item = self.cart[str(product.id)]
            items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': Decimal(item['price']),
                'subtotal': Decimal(item['price']) * item['quantity'],
            })
        return items

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
