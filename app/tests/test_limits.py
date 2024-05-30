import nanoid
from services.limits import is_rate_limited


def test_is_rate_limited():
    key = "test" + nanoid.generate()
    limit = 5
    window = 3
    for _ in range(limit):
        assert not is_rate_limited(key, limit, window)
    assert is_rate_limited(key, limit, window)
