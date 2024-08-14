from decimal import Decimal

from django.conf import settings

from products.serializers import ProductSerializer
from products.models import Product


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product_uuid):
        if product_uuid not in self.cart:
            self.cart[product_uuid] = {
                "quantity": 1,
                "price": 1 # just for initialization will be updated later in the __iter__()
            }
        self.save()
        
    def increament(self, product_uuid):
        product = Product.objects.get(uuid=product_uuid)
        if  (product_uuid in self.cart) and (product.stock > self.cart[product_uuid]["quantity"]):
            self.cart[product_uuid]["quantity"] += 1
            self.save()
            
    def decreament(self, product_uuid):
        if (product_uuid in self.cart) and (self.cart[product_uuid]["quantity"] > 1):
            self.cart[product_uuid]["quantity"] -= 1
            self.save()
            
    def update(self, product_uuid, quantity):
        product = Product.objects.get(uuid=product_uuid)
        if  (product_uuid in self.cart) and (product.stock > int(quantity) + self.cart[product_uuid]["quantity"]):
            self.cart[product_uuid]["quantity"] += int(quantity)
        else:
            self.cart[product_uuid]["quantity"] = product.stock
        self.save()

    def remove(self, product_uuid):
        if product_uuid in self.cart:
            del self.cart[product_uuid]
            self.save()

    def __iter__(self):
        """
        Loop through cart items and fetch the products from the database
        """
        product_uuids = self.cart.keys()
        print(product_uuids)
        products = Product.objects.filter(uuid__in=product_uuids)
        print(products)
        cart = self.cart.copy()
        for product in products:
            cart_item = cart[str(product.uuid)]
            cart_item["product"] = ProductSerializer(product).data
            cart_item["price"] = product.price #add the price k,v to the dict
            cart_item["total_price"] = product.price * cart_item["quantity"] #add the total_price k,v to the dict
            
            self.cart[str(product.uuid)]["price"] = product.price #updates the price per product in the cart field of this class instance
            yield cart_item


    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()