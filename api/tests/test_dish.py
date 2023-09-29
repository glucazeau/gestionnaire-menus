import pytest

from hamcrest import assert_that, equal_to
from unittest.mock import Mock, patch

from dish import pick_dish

p = pytest.param


def validate_dish_mock_return(dish, meal, day, week):
    if dish.id == 3:
        return True, "OK"
    else:
        return False, "KO"


def test_pick_dish__first_valid_dish_is_returned():
    dish1 = Mock(name="dish_1")
    dish1.id = 1
    dish2 = Mock(name="dish_2")
    dish2.id = 2
    dish3 = Mock(name="dish_3")
    dish3.id = 3
    dish4 = Mock(name="dish_4")
    dish4.id = 4

    dishes = [dish1, dish2, dish3, dish4]

    week = Mock()
    day = Mock()
    meal = Mock()

    with patch("dish.validate_dish") as validator_mock:
        validator_mock.side_effect = validate_dish_mock_return

        chosen_dish = pick_dish(week, day, meal, dishes)

        assert_that(
            chosen_dish,
            equal_to(dish3),
        )
