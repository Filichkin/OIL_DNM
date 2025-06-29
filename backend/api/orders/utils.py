def generate_order_number(dealer, supplier: str):
    order_number = str(dealer) + supplier + str(0) * (
            6 - len(str(dealer.orders.count()))
            ) + str(dealer.orders.count())
    return order_number
