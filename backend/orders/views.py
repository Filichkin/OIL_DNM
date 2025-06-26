order_lemark = Order.objects.create(
            rs_code=rs_code,
            comment=comment,
            **validated_data
        )
order_avtomarket = Order.objects.create(
            rs_code=rs_code,
            comment=comment,
            **validated_data
        )
for item in cart.items:
    if item['brand'] == 'Lemarc':
        lemark_order_number = item['dealer'] + 'L' + order_lemark.id
        order_lemark.order_number = lemark_order_number
        order_lemark.save()
        OrderItem.objects.create(
                    order=order_lemark,
                    product=item['product'],
                    price=item['price'],
                    count=item['quantity']
                )
    avtomarket_order_number = item['dealer'] + 'A' + order_avtomarket.id
    order_avtomarket.order_number = avtomarket_order_number
    order_avtomarket.save()
    OrderItem.objects.create(
                    order=order_avtomarket,
                    product=item['product'],
                    price=item['price'],
                    count=item['quantity']
                )
if not lemark_order_number:
    del order_lemark
elif not avtomarket_order_number:
    del order_avtomarket
