# from dishorder import session
# from dishorder.views.models import *
# import threading
# import datetime
#
#
# def automate_create_order():
#     curent_day = datetime.datetime.now()
#     timestamp_of_this_day = get_timestamp_by(7, 1)
#     one_day = 60 * 60 * 24
#     suppliers = session.query(Suppliers).all()
#     for supplier in suppliers:
#         dish_order_by_supplier = session.query(CustomerOrders, Dishes) \
#             .join(Dishes, CustomerOrders.dish_id == Dishes.dish_id) \
#             .filter(Dishes.supplier_code == supplier.code)\
#             .filter(CustomerOrders.order_date >= timestamp_of_this_day)\
#             .filter(CustomerOrders.order_date < timestamp_of_this_day + one_day).all()
#         for dish in dish_order_by_supplier:
#             new_order_to_supplier = OrdersToSuppliers(supplier_code=supplier.code,
#                                                       order_date=timestamp_of_this_day,
#                                                       delivery_address="DI",
#                                                       total_amount=
#                                                       )
#             session.query(OrdersToSuppliers)
#
#
# thread = threading.Thread(target=automate_create_order)
# thread.start()
from dishorder import session
from dishorder.views.models import *


def update_order_to_supplier(order_id):
    one_day = 60 * 60 * 24
    suppliers = session.query(Suppliers).all()
    orders = session.query(CustomerOrders, Dishes) \
        .join(Dishes, CustomerOrders.dish_id == Dishes.dish_id) \
        .filter(CustomerOrders.order_id == order_id).all()
    total_sum = 0
    for order in orders:
        print(order)
        total_sum = total_sum + (order[0].quantity * order[0].unit_price)
    update_order = session.query(OrdersToSuppliers).filter(OrdersToSuppliers.order_id == order_id).first()
    update_order.total_amount = total_sum
    session.commit()
