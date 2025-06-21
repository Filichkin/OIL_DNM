from decimal import Decimal

from django.conf import settings

from catalog.models import Catalog


class Cart:
    def __init__(self, request):
        '''Создание корзины'''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, count=1, override_count=False):
        '''
        Добавление товара в корзину
        или обновление его количества
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'count': 0,
                'price': str(product.price)
            }
        if override_count:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        '''Удаление товара из корзины'''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''
        Прокрутка товаров корзине и
        получение товаров из базы данных
        '''
        product_ids = self.cart.keys()
        products = Catalog.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
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
