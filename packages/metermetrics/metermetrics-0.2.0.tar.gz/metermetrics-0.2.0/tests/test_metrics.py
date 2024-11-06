from metermetrics.counter import Counter


def test_counter():
    counter = Counter(1)
    counter.add_val(1, 2)
    print(counter.get_last_err(True))
