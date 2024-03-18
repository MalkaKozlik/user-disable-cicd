from unittest.mock import patch, Mock
import json
import pytest
import requests

from project.update_user_attribute import update_user_attribute, remove_user_attribute


class response:
    def __init__(self, status_code):
        self.status_code = status_code


@patch.object(requests, "patch", return_value=response(204))
def test_update_user_attribute_called_patch(mock_patch):
    update_user_attribute(
        "access_token", "user_id", "attribute_name", "attribute_value"
    )
    mock_patch.assert_called_once_with(
        "https://graph.microsoft.com/v1.0/users/user_id",
        headers={
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
        data=json.dumps({"attribute_name": "attribute_value"}),
    )


@patch("project.update_user_attribute.requests.patch", Mock(return_value=response(403)))
def test_update_user_attribute_raise_exception():
    with pytest.raises(Exception) as exception:
        update_user_attribute(
            "access_token", "user_id", "attribute_name", "attribute_value"
        )
    assert "The status code is: 403" in str(exception.value)


@patch("project.update_user_attribute.update_user_attribute")
def test_remove_user_attribute(update_user_attribute):
    remove_user_attribute("access_token", "user_id", "attribute_name")
    update_user_attribute.assert_called_once_with(
        "access_token", "user_id", "attribute_name", None
    )
