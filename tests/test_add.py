import pytest


def add(a, b):
    return a + b


@pytest.mark.parametrize("a,b,expected",
                         [
                             (1, 2, 3),
                             (2, 4, 6),
                             (-1, 1, 0),
                             (-2, 2, 0)
                         ]
                         )
def test_add_1(a, b, expected):
    result = add(a, b)

    assert result == expected
