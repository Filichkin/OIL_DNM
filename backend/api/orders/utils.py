def generate_order_number(dealer, supplier: str):
    order_number = str(dealer) + supplier + str(0) * (
            6 - len(str(
                dealer.orders.filter(order_number__contains=supplier).count()
                )
            )
        ) + str(
            dealer.orders.filter(order_number__contains=supplier).count() + 1
            )
    return order_number
