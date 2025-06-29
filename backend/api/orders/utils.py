def generate_order_number(dealer):
    order_number = str(dealer) + str(0) * (
            6 - len(str(dealer.orders.count()))
            ) + str(dealer.orders.count())
    return order_number
