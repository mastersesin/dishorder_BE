import threading
import sys
import time
from dishorder import session
from dishorder.views.models import *


while True:
    all_orders = session.query(CustomerOrders).all()
    print(all_orders)
    time.sleep(5)
