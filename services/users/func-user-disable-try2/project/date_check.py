import datetime

from project.update_user_attribute import update_user_attribute, remove_user_attribute


def is_past_expiration_by(days: int, date, access_token, user_id, attribute_name):
    desired_date = adding_days_to_date(days, date)
    date = convert_datetime_to_date(desired_date)
    disable_user_by_expiration(date, access_token, user_id, attribute_name)


def adding_days_to_date(days: int, date):
    required_date = date + datetime.timedelta(days=int(days))
    return required_date


def disable_user_by_expiration(date, access_token, user_id, attribute_name):
    if datetime.date.today() > date:
        try:
            update_user_attribute(access_token, user_id, "accountEnabled", "false")
            remove_user_attribute(access_token, user_id, attribute_name)
        except Exception:
            return


def convert_datetime_to_date(date):
    return datetime.date(date.year, date.month, date.day)
