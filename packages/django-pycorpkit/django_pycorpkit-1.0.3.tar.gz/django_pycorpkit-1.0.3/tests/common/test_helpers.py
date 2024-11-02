import pytest

from pycorpkit.common.utils.exceptions import InvalidPhoneNumber
from pycorpkit.common.utils.helpers import validate_a_phone_number


def test_valid_kenya_phone_number():
    phone_number = "+254712345678"
    result = validate_a_phone_number(phone_number, "KE")
    assert result == phone_number


def test_valid_usa_phone_number():
    phone_number = "+14155552671"
    result = validate_a_phone_number(phone_number, "US")
    assert result == phone_number


def test_invalid_phone_number_format():
    phone_number = "12345"
    with pytest.raises(InvalidPhoneNumber) as exc_info:
        validate_a_phone_number(phone_number, "KE")
    assert str(exc_info.value) == "'12345' is not a valid phone number"


def test_invalid_phone_number_length():
    phone_number = "+25471234"
    with pytest.raises(InvalidPhoneNumber) as exc_info:
        validate_a_phone_number(phone_number, "KE")
    assert str(exc_info.value) == "'+25471234' is not a valid phone number"


def test_invalid_country_code():
    phone_number = "+9876543210"
    with pytest.raises(InvalidPhoneNumber) as exc_info:
        validate_a_phone_number(phone_number, "ZZ")
    assert str(exc_info.value) == "'+9876543210' is not a valid phone number"


def test_number_parse_exception():
    phone_number = "NotAPhoneNumber"
    with pytest.raises(InvalidPhoneNumber) as exc_info:
        validate_a_phone_number(phone_number, "KE")
    assert str(exc_info.value) == "'NotAPhoneNumber' is not a valid phone number"
