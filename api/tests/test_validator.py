import pytest

from hamcrest import assert_that, equal_to
from unittest.mock import MagicMock, patch

from validator import NoLongDishOnWeekDay

p = pytest.param


@pytest.mark.parametrize(
    "long_to_prepare, is_week_day, expected",
    [
        p(
            False,
            True,
            True,
            id="Dish is not long and day is a week day - dish is valid",
        ),
        p(
            False,
            False,
            True,
            id="Dish is not long and day is not a week day - dish is valid",
        ),
        p(
            True,
            True,
            False,
            id="Dish is long and day is a week day - dish is not valid",
        ),
        p(
            True,
            False,
            True,
            id="Dish is long and day is a not week day - dish is valid",
        ),
    ],
)
def test_rule_not_long_dish_on_weekday(long_to_prepare, is_week_day, expected):
    rule = NoLongDishOnWeekDay()

    day = MagicMock()
    day.is_weekend.return_value = not is_week_day

    with patch("models.Dish") as dish_mock:
        dish_mock.return_value.is_long_to_prepare = long_to_prepare

    rule = NoLongDishOnWeekDay()
    assert_that(
        rule.valid(dish_mock.return_value, day, MagicMock()),
        equal_to(expected),
    )
