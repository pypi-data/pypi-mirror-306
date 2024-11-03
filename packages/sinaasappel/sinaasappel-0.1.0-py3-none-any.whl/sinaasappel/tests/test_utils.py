import typing as t

import pytest

from sinaasappel import recursive_sum


@pytest.mark.parametrize(
    "input_list,expected",
    [
        (1, 1),
        ([1], 1),
        ([1, 2, [3, [4]]], 10),
        ([[[[[[[[[[19]]]]]]]]]], 19),
        ([[1, 2, 3, 4], [1, 2, 3, 4]], 20),
    ],
)
def test_recursive_sum(
    input_list: t.Union[int, list[t.Union[int, list]]], expected: int
):
    assert recursive_sum(input_list) == expected
