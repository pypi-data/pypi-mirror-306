import time

from buffr.buffers import Buffr


def test_buffer_flushes_when_at_capacity():
    required_number_of_items = 5

    buffr = Buffr(max_capacity=required_number_of_items, buffer_ttl=1, flush_func=print)
    for i in range(required_number_of_items - 1):
        buffr.add(i)

    assert buffr.size == required_number_of_items - 1
    buffr.add(9)
    assert buffr.size == 0


def test_buffer_flushes_when_expired():
    buffr = Buffr(max_capacity=100, buffer_ttl=0.1, flush_func=print)
    for i in range(3):
        buffr.add(i)

    assert buffr.size == 3
    time.sleep(0.3)
    assert buffr.size == 0


def test_can_stop_timeout_clock():
    buffr = Buffr(max_capacity=100, buffer_ttl=0.2, flush_func=print)
    for i in range(3):
        buffr.add(i)

    assert buffr.size == 3
    buffr.stop()
    time.sleep(0.3)
    assert buffr.size == 3


if __name__ == "__main__":
    test_buffer_flushes_when_expired()

"""
python -m  coverage run --omit="test/*" -m pytest 
coverage html
start chrome %cd%/htmlcov/index.html
"""
