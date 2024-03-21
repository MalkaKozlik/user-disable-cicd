import datetime

from project.user_attribute import update_user_attribute, remove_user_attribute


def is_past_expiration_by(days: int, date, access_token, user_id, attribute_name):
    desired_date = add_days(date, days)
    date = convert_datetime_to_date(desired_date)
    disable_user(date, access_token, user_id, attribute_name)


def add_days(date, days: int):
    required_date = date + datetime.timedelta(days=int(days))
    return required_date


def disable_user(date, access_token, user_id, attribute_name):
    if datetime.date.today() > date:
        try:
            update_user_attribute(access_token, user_id, "accountEnabled", "false")
            remove_user_attribute(access_token, user_id, attribute_name)
        except Exception:
            return


def convert_datetime_to_date(date):
    return datetime.date(date.year, date.month, date.day)
