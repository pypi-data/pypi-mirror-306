from buffr.buffers import Buffr


def test_can_read_buffer_size():
    buffr = Buffr(max_capacity=100, buffer_ttl=1, flush_func=print)
    for i in range(4):
        buffr.add(i)
    assert buffr.size == 4

    buffr.add(1)
    assert buffr.size == 5

    buffr.flush()
    assert buffr.size == 0


def test_correct_str():
    buffr = Buffr(max_capacity=100, buffer_ttl=1, flush_func=print)
    for i in range(4):
        buffr.add(i)
    print(str(buffr))
    assert (
        str(buffr)
        == f"<Buffr capacity={buffr.size}/{buffr.max_capacity}, TTL={buffr._buffer_ttl}s>"
    )


"""
uv run coverage run --omit="test/*" -m pytest
python -m coverage run --omit="test/*" -m pytest 
coverage html
start chrome %cd%/htmlcov/index.html
"""
