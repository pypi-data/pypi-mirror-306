import phonenumbers

from pycorpkit.common.utils.conf import SETTINGS
from pycorpkit.common.utils.exceptions import InvalidPhoneNumber


def format_error_response(*, message, status_code):
    error_message = {"detail": message}
    if isinstance(message, dict):
        consolidated_message = " ".join(
            f"{key}: {detail}" for key, value in message.items() for detail in value
        )
        error_message["detail"] = consolidated_message
    return error_message, status_code


def validate_a_phone_number(phone_number, country="KE"):
    error = "'{}' is not a valid phone number".format(phone_number)

    try:
        parsed_number = phonenumbers.parse(phone_number, country)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise InvalidPhoneNumber(error)

    if not phonenumbers.is_valid_number(parsed_number):
        raise InvalidPhoneNumber(error)

    return phonenumbers.format_number(
        parsed_number, phonenumbers.PhoneNumberFormat.E164
    )


def get_default_roles():
    return SETTINGS["DEFAULT_ROLES"]


PERMS = SETTINGS["PERMISSIONS_PATH"]
