from decimal import Decimal

from django.conf import settings

from catalog.models import Catalog


class Cart:
    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, dealer, count=1, override_count=False):

        product_id = str(product.id)
        dealer = str(dealer)
        if dealer not in self.cart:
            self.cart[dealer] = {}
        if product_id not in self.cart[dealer]:
            self.cart[dealer][product_id] = {
                'count': 0,
                'brand': str(product.brand),
                'price_per_box': str(product.price_per_box),
                'product_name': str(product.name),
                'part_number': str(product.part_number),
                'volume': str(product.volume),
                'product_id': product_id,
                'dealer': dealer,
                }
        if override_count:
            self.cart[dealer][product_id]['count'] = count
        else:
            self.cart[dealer][product_id]['count'] += count
        self.save()
        # print(self.cart)

    def save(self):
        self.session.modified = True

    def remove(self, product_id, dealer):

        product_id = str(product_id)
        dealer = str(dealer)
        if product_id in self.cart[dealer]:
            del self.cart[dealer][product_id]
            self.save()

    def __iter__(self):
        cart = self.cart.copy()
        for dealer in self.cart.keys():

            product_ids = self.cart[dealer].keys()
            products = Catalog.objects.filter(id__in=product_ids)

            for product in products:
                cart[dealer][str(product.id)]['product'] = product
            for item in cart[dealer].values():
                item['dealer'] = item['dealer']
                item['product_id'] = item['product_id']
                item['product_name'] = item['product_name']
                item['brand'] = item['brand']
                item['part_number'] = item['part_number']
                item['volume'] = item['volume']
                item['price_per_box'] = Decimal(item['price_per_box'])
                item['total_price'] = item['price_per_box'] * item['count']
                yield item

    def __len__(self):
        '''Подсчет количества позиций в корзине'''
        return sum(item['count'] for item in self.cart.values())

    def get_total_price(self):
        '''Расчет общей стоимости товаров'''
        return sum(
            Decimal(item['price_per_box']) * item['count']
            for item in self.cart.values()
        )

    def clear(self):
        '''Удаление корзины из сеанса'''
        del self.session[settings.CART_SESSION_ID]
        self.save

    def get_cart_items(self):
        return self

    def get_cart_items_list(self) -> list:
        # Return cart items in a structured format for API serialization
        items = []
        for product_id, item in self.cart.items():
            get_item = self.get_item(product_id=product_id, item=item)
            if get_item is None:
                continue
            items.append(get_item)

        return items

    def get_item(self, product_id: int, item=None) -> dict:
        item = item or self.cart.get(str(product_id))
        if item is None:
            return None
        try:
            product = Catalog.objects.get(id=int(product_id))
            item_data = {
                'product_id': product_id,
                'product_name': product.name,
                'count': item['count'],
                'price': str(item['price']),
                'total_price': str(
                    Decimal(item['price_per_box']) * int(item['count'])
                    ),
            }
            return item_data
        except Catalog.DoesNotExist:
            pass
        return None
