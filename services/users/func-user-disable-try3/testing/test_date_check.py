from unittest.mock import patch, Mock
from datetime import date, timedelta, datetime

from project.date_check import (
    is_past_expiration_by,
    add_days,
    disable_user,
    convert_datetime_to_date,
)


@patch("project.date_check.add_days", Mock(return_value=date(2023, 1, 1)))
@patch(
    "project.date_check.convert_datetime_to_date", Mock(return_value=date(2023, 1, 1))
)
@patch("project.date_check.disable_user")
def test_is_past_expiration_by_assert_called_disable_user(
    disable_user,
):
    is_past_expiration_by(
        3, date(2023, 1, 1), "access_token", "user_id", "application_id"
    )
    disable_user.assert_called_once_with(
        date(2023, 1, 1), "access_token", "user_id", "application_id"
    )


@patch("project.date_check.disable_user", Mock(return_value=True))
@patch(
    "project.date_check.convert_datetime_to_date", Mock(return_value=date(2023, 1, 1))
)
@patch("project.date_check.add_days")
def test_is_past_expiration_by_assert_called_add_days(add_days):
    is_past_expiration_by(
        3, date(2023, 1, 1), "access_token", "user_id", "application_id"
    )
    add_days.assert_called_once_with(date(2023, 1, 1), 3)


@patch(
    "project.date_check.datetime.timedelta",
    Mock(return_value=timedelta(seconds=259200)),
)
def test_add_days():
    assert add_days(date(2023, 1, 1), 3) == date(2023, 1, 4)


@patch(
    "project.date_check.datetime.date",
    Mock(**{"today.return_value": date(2023, 11, 6)}),
)
@patch("project.date_check.remove_user_attribute", Mock(return_value=None))
@patch("project.date_check.update_user_attribute")
def test_disable_user_assert_called_update_user(update_user_attribute):
    disable_user(date(2023, 1, 1), "access_token", "user_id", "application_id")
    update_user_attribute.assert_called_once_with(
        "access_token", "user_id", "accountEnabled", "false"
    )


@patch(
    "project.date_check.datetime.date",
    Mock(**{"today.return_value": date(2023, 11, 6)}),
)
@patch("project.date_check.update_user_attribute", Mock(return_value=None))
@patch("project.date_check.remove_user_attribute")
def test_disable_user_assert_called_remove_user(remove_user_attribute):
    disable_user(date(2023, 1, 1), "access_token", "user_id", "application_id")
    remove_user_attribute.assert_called_once_with(
        "access_token", "user_id", "application_id"
    )


@patch(
    "project.date_check.datetime.date",
    Mock(**{"today.return_value": date(2023, 11, 6)}),
)
@patch("project.date_check.update_user_attribute", Mock(side_effect=Exception()))
def test_disable_user_return_exception():
    assert (
        disable_user(date(2023, 1, 1), "access_token", "user_id", "application_id")
        is None
    )


def test_convert_datetime_to_date():
    assert convert_datetime_to_date(datetime(2023, 11, 29)) == date(2023, 11, 29)
