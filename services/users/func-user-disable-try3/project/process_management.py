from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import requests
import datetime

from project.date_check import is_past_expiration_by
from project.user_attribute import update_user_attribute
from project.ad_users import users_by_department
from config.config_variables import (
    tenant_id,
    client_id,
    client_secret,
    application_id,
    keyvault_uri,
    department,
    days,
)


def inspection_process_management():
    access_token, application_id_value = get_access_token_and_app_id()
    if access_token:
        try:
            send_users_for_testing(access_token, department, days, application_id_value)
        except Exception:
            return "send_users_for_testing does not succeed"
    else:
        return "Failed to obtain access token"


def get_access_token_and_app_id():
    secret_client = get_secret_client(keyvault_uri)
    tenant_id_value = get_kv_value_secret(secret_client, tenant_id)
    client_id_value = get_kv_value_secret(secret_client, client_id)
    client_secret_value = get_kv_value_secret(secret_client, client_secret)
    application_id_value = get_kv_value_secret(secret_client, application_id)
    access_token = get_access_token(
        tenant_id_value, client_id_value, client_secret_value
    )
    return access_token, application_id_value


def get_secret_client(KVUri):
    return SecretClient(vault_url=KVUri, credential=DefaultAzureCredential())


def get_kv_value_secret(secretClient, secret_name):
    return secretClient.get_secret(secret_name).value


def get_access_token(tenant_id, client_id, client_secret):
    try:
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default",
        }
        response = requests.post(url, headers=headers, data=data)
        access_token = response.json().get("access_token")
        return access_token
    except Exception:
        raise Exception("Failed to get access token")


def send_users_for_testing(access_token, department, days, application_id):
    users = users_by_department(
        access_token, department, "extension_" + application_id + "_expiration_date"
    )
    for user in users:
        print(user['id'])
        user['id'] = "d6075f16-f3c7-4545-9b49-8718ee53dbcb"
        check_user_expiration_date(access_token, user, days, application_id)


def check_user_expiration_date(access_token, user, days, application_id):
    attribute_name = f"extension_{application_id}_expiration_date"
    if attribute_name in user:
        is_past_expiration_by(
            days,
            datetime.datetime.fromisoformat(user[attribute_name]),
            access_token,
            user["id"],
            attribute_name,
        )
    else:
        update_user_attribute(
            access_token, user["id"], attribute_name, datetime.date.today().isoformat()
        )
