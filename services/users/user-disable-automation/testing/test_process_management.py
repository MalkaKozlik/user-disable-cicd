from unittest.mock import patch, Mock, call
import pytest

from project.process_management import (
    get_access_token,
    user_expiration_date_check,
    sending_users_for_testing,
    inspection_process_management,
    get_access_token_and_app_id,
    kv_get_value_secret,
)


@patch(
    "project.process_management.requests.post",
    Mock(side_effect=Exception("Failed to get access token")),
)
def test_get_access_token_raise_exception():
    with pytest.raises(Exception) as exception:
        get_access_token("tenant_id", "client_id", "client_secret")
    assert "Failed to get access token" in str(exception.value)


@patch("project.process_management.requests.post")
def test_get_access_token_called_post(post):
    get_access_token("tenant_id", "client_id", "client_secret")
    post.called_assert_once_with(
        "https://login.microsoftonline.com/tenant_id/oauth2/v2.0/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": "client_id",
            "client_secret": "client_secret",
            "scope": "https://graph.microsoft.com/.default",
        },
    )


@patch("project.process_management.is_past_expiration_by")
def test_user_expiration_date_check_assert_called_check_if_x_days_passed_since_expiration_date(
    is_past_expiration_by,
):
    user_expiration_date_check(
        "access_token",
        {"id": "id", "extension_application_id_expiration_date": "2023-12-03"},
        3,
        "application_id",
    )
    is_past_expiration_by.called_assert_once_with(
        "access_token", "id", "2023-12-03", 3, "application_id"
    )


@patch("project.process_management.update_user_attribute")
def test_user_expiration_date_check_assert_called_add_property_to_user(
    update_user_attribute,
):
    user_expiration_date_check("access_token", {"id": "id"}, 3, "application_id")
    update_user_attribute.called_assert_once_with(
        "access_token", "id", "expiration_date", "12/03/2023", "application_id"
    )


@patch(
    "project.process_management.retrieving_users_by_department_name",
    Mock(return_value=[{"id": "aaa"}, {"id": "bbb"}]),
)
@patch("project.process_management.user_expiration_date_check")
def test_sending_users_for_testing_called_user_expiration_date_check(
    user_expiration_date_check,
):
    sending_users_for_testing("access_token", "department", 3, "application_id")
    assert user_expiration_date_check.call_count == 2


@patch(
    "project.process_management.get_access_token_and_app_id",
    Mock(return_value=("access_token", "application_id")),
)
@patch("project.process_management.sending_users_for_testing")
def test_inspection_process_management_assert_called_sending_users_for_testing(
    sending_users_for_testing,
):
    inspection_process_management()
    sending_users_for_testing.called_assert_once_with(
        "access_token", "department", 3, "application_id"
    )


@patch(
    "project.process_management.get_access_token_and_app_id",
    Mock(return_value=("", "app_id")),
)
def test_inspection_process_management_return_failed():
    assert (
        inspection_process_management()
        == "Failed to obtain access token"
    )


@patch(
    "project.process_management.get_access_token_and_app_id",
    Mock(return_value=("access_token", "application_id")),
)
@patch(
    "project.process_management.sending_users_for_testing",
    Mock(side_effect=Exception()),
)
def test_inspection_process_management_return():
    assert (
        inspection_process_management()
        == "sending_users_for_testing does not succeed"
    )


@patch("project.process_management.keyvault_uri", "keyvault_uri")
@patch("project.process_management.tenant_id", "tenant_id")
@patch("project.process_management.client_id", "client_id")
@patch("project.process_management.client_secret", "client_secret")
@patch("project.process_management.application_id", "application_id")
@patch("project.process_management.get_access_token", Mock(return_value="access_token"))
@patch(
    "project.process_management.get_secret_client", Mock(return_value="secret_client")
)
@patch("project.process_management.kv_get_value_secret")
def test_get_access_token_and_app_id(kv_get_value_secret):
    get_access_token_and_app_id()
    calls = [
        call("secret_client", "tenant_id"),
        call("secret_client", "client_id"),
        call("secret_client", "client_secret"),
        call("secret_client", "application_id"),
    ]
    kv_get_value_secret.assert_has_calls(calls)


class secret:
    def __init__(self):
        self.value = "secret"


class client:
    def get_secret(vault_url, creditionals):
        return secret()


def test_kv_get_value_secret():
    assert kv_get_value_secret(client(), "secret_name") == ("secret")
