import requests


def retrieving_users_by_department_name(access_token, department, expiration_date):
    select, filter, top = setting_up_data_for_receiving_users(
        department, expiration_date
    )
    users = get_users(access_token, select, filter, top)
    return users["value"]


def setting_up_data_for_receiving_users(department, expiration_date):
    select = f"id,{expiration_date}"
    filter = f"Department in ('{department}') and accountEnabled+eq+true"
    top = 999
    return select, filter, top


def get_users(access_token, select, filter, top):
    try:
        url = f"https://graph.microsoft.com/v1.0/users?$select={select}&$filter={filter}&$top={top}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "ConsistencyLevel": "eventual",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception:
        raise Exception("Failed to get users")
