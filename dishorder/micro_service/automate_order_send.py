import threading
import sys
import time


def test(*args):
    print(args)
    while True:
        a = 0
        for i in range(10):
            a = a + 1


for i in range(20):
    thread = threading.Thread(target=test, args=[i])
    thread.start()
