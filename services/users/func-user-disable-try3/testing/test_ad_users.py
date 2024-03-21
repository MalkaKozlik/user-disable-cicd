from unittest.mock import patch, Mock
import pytest

from project.ad_users import (
    get_users,
    users_by_department,
    set_up_data_for_receiving_users,
)


@patch("project.ad_users.requests.get")
def test_get_users_called_requests_get_with_parameters(get):
    get_users("access_token", "select", "filter", "top")
    get.assert_called_once_with(
        "https://graph.microsoft.com/v1.0/users?$select=select&$filter=filter&$top=top",
        headers={
            "Authorization": "Bearer access_token",
            "ConsistencyLevel": "eventual",
            "Content-Type": "application/json",
        },
    )


@patch(
    "project.ad_users.requests.get",
    Mock(side_effect=Exception("Failed to get users")),
)
def test_get_users_raise_exception():
    with pytest.raises(Exception) as exception:
        get_users("access_token", "select", "filter", "top")
    assert "Failed to get users" in str(exception.value)


@patch(
    "project.ad_users.set_up_data_for_receiving_users",
    Mock(return_value=("select", "filter", 0)),
)
@patch(
    "project.ad_users.get_users",
    Mock(return_value={"value": [{"id": 0}, {"id": 1}]}),
)
def test_users_by_department():
    assert users_by_department("access_token", "department", "expiration_date") == [
        {"id": 0},
        {"id": 1},
    ]


def test_set_up_data_for_receiving_users():
    assert set_up_data_for_receiving_users("test", "expiration_date") == (
        "id,expiration_date",
        "Department in ('test') and accountEnabled+eq+true",
        999,
    )
