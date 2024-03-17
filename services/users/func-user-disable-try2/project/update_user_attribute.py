import requests
import json


def update_user_attribute(access_token, user_id, attribute_name, attribute_value):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = json.dumps({attribute_name: attribute_value})
    response = requests.patch(url, headers=headers, data=data)
    if response.status_code != 204:
        raise Exception("The status code is: " + str(response.status_code))


def remove_user_attribute(access_token, user_id, attribute_name):
    return update_user_attribute(access_token, user_id, attribute_name, None)
