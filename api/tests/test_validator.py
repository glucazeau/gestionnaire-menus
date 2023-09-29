import pytest

from hamcrest import assert_that, equal_to
from unittest.mock import MagicMock, patch

from validator import NoLongDishOnWeekDay, PaidDishOnlyOnWeekendNights
from models import MealMoment

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
    day = MagicMock()
    day.is_weekend.return_value = not is_week_day

    with patch("models.Dish") as dish_mock:
        dish_mock.return_value.is_long_to_prepare = long_to_prepare

    rule = NoLongDishOnWeekDay()

    assert_that(
        rule.valid(dish_mock.return_value, MagicMock(), day, MagicMock()),
        equal_to(expected),
    )


@pytest.mark.parametrize(
    "from_restaurant, is_weekend, meal_type, expected",
    [
        p(
            False,
            False,
            MealMoment.Midi,
            True,
            id="Dish is not paid and meal is lunch on weekday - dish is valid",
        ),
        p(
            True,
            False,
            MealMoment.Midi,
            False,
            id="Dish is paid and meal is lunch on weekday - dish is not valid",
        ),
        p(
            False,
            False,
            MealMoment.Soir,
            True,
            id="Dish is not paid and meal is dinner on weekday - dish is valid",
        ),
        p(
            True,
            False,
            MealMoment.Soir,
            False,
            id="Dish is paid and meal is dinner on weekday - dish is not valid",
        ),
        p(
            False,
            True,
            MealMoment.Midi,
            True,
            id="Dish is not paid and meal is lunch on weekend - dish is valid",
        ),
        p(
            True,
            True,
            MealMoment.Midi,
            False,
            id="Dish is paid and meal is lunch on weekend - dish is not valid",
        ),
        p(
            False,
            True,
            MealMoment.Soir,
            True,
            id="Dish is not paid and meal is dinner on weekend - dish is valid",
        ),
        p(
            True,
            True,
            MealMoment.Soir,
            True,
            id="Dish is paid and meal is dinner on weekend - dish is valid",
        ),
        p(
            True,
            True,
            MealMoment.Soir,
            True,
            id="Dish is paid and meal is lunch on Friday - dish is valid",
        ),
    ],
)
def test_rule_no_paid_dish_on_weekday(from_restaurant, is_weekend, meal_type, expected):
    with patch("models.Day") as day_mock:
        day_mock.return_value.is_weekend.return_value = is_weekend
        if is_weekend:
            day_mock.return_value.number = 6
        else:
            day_mock.return_value.number = 1

        with patch("models.Meal") as meal_mock:
            meal_mock.return_value.type = meal_type

            with patch("models.Dish") as dish_mock:
                dish_mock.return_value.from_restaurant = from_restaurant

    rule = PaidDishOnlyOnWeekendNights()
    assert_that(
        rule.valid(
            dish_mock.return_value,
            meal_mock.return_value,
            day_mock.return_value,
            MagicMock(),
        ),
        equal_to(expected),
    )


@pytest.mark.parametrize(
    "from_restaurant, meal_type, expected",
    [
        p(
            True,
            MealMoment.Midi,
            False,
            id="Dish is paid and meal is lunch on Friday - dish is not valid",
        ),
        p(
            True,
            MealMoment.Soir,
            True,
            id="Dish is paid and meal is dinner on Friday - dish is valid",
        ),
        p(
            False,
            MealMoment.Midi,
            True,
            id="Dish is not paid and meal is lunch on Friday - dish is valid",
        ),
        p(
            False,
            MealMoment.Soir,
            True,
            id="Dish is not paid and meal is dinner on Friday - dish is valid",
        ),
    ],
)
def test_rule_paid_dish_ok_on_friday_night(from_restaurant, meal_type, expected):
    with patch("models.Day") as day_mock:
        day_mock.return_value.number = 5
        day_mock.return_value.is_weekend.return_value = False

        with patch("models.Meal") as meal_mock:
            meal_mock.return_value.type = meal_type

            with patch("models.Dish") as dish_mock:
                dish_mock.return_value.from_restaurant = from_restaurant

    rule = PaidDishOnlyOnWeekendNights()
    assert_that(
        rule.valid(
            dish_mock.return_value,
            meal_mock.return_value,
            day_mock.return_value,
            MagicMock(),
        ),
        equal_to(expected),
    )
