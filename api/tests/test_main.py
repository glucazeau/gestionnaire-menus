import pytest

from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to
from unittest.mock import Mock, patch

import models

from main import app, get_db
from week import WeekStatus

p = pytest.param

client = TestClient(app)

db_mock = Mock()

app.dependency_overrides[get_db] = lambda: db_mock


@pytest.mark.parametrize(
    "action, expected_status, expected_code",
    [
        p(
            "save",
            WeekStatus.SAVED,
            200,
            id="Action is save - set status to SAVED and returns 200",
        ),
        p(
            "edit",
            WeekStatus.DRAFT,
            200,
            id="Action is save - set status to DRAFT and returns 200",
        ),
        p(
            "unknown",
            WeekStatus.DRAFT,
            422,
            id="Action is not edit nor save - returns 422",
        ),
    ],
)
@patch("week.get_week_menus")
@patch("week.set_week_status")
def test_week_action_endpoint(
    set_week_status_mock, get_week_menus_mock, action, expected_status, expected_code
):
    get_week_menus_mock.return_value = models.Week(
        year=2023, number=39, days=[], status=expected_status.value
    )

    response = client.post("/week/2023/39", json={"action": action})
    assert_that(response.status_code, equal_to(expected_code))

    if expected_status == 200:
        set_week_status_mock.assert_called_with(db_mock, "2023", "39", expected_status)
        assert_that(
            response.json(),
            equal_to(
                {
                    "year": 2023,
                    "number": 39,
                    "days": [],
                    "status": expected_status.name,
                    "is_current": False,
                    "is_finished": True,
                }
            ),
        )
