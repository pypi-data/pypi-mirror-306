from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from pycorpkit.common.utils.conf import SETTINGS
from pycorpkit.common.utils.error_codes import ErrorCodes
from pycorpkit.common.utils.helpers import format_error_response


def create_access_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    refresh_token = refresh

    access_token_life_time = SETTINGS["SIMPLE_JWT"]["ACCESS_TOKEN_LIFETIME"]
    access_token["iat"] = int(timezone.now().timestamp())
    access_token["exp"] = timezone.now() + timedelta(
        seconds=access_token_life_time.total_seconds()
    )
    access_token["user_id"] = user.id

    refresh_token["iat"] = int(timezone.now().timestamp())
    refresh_token["exp"] = timezone.now() + timedelta(
        seconds=access_token_life_time.total_seconds()
    )
    refresh_token["user_id"] = user.id

    return str(access_token), str(refresh_token)


@transaction.atomic
def authenticate_user(email=None, phone=None, password=None):
    if email:
        user = authenticate(username=email, password=password)
    else:
        user = authenticate(phone=phone, password=password)

    if not user:
        return format_error_response(
            message=ErrorCodes.INCORRECT_LOGIN_CREDENTIALS.value,
            status_code=HTTPStatus.BAD_REQUEST,
        )

    access_token, refresh_token = create_access_token(user=user)

    data = {
        "user": user,
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    }
    return data, HTTPStatus.OK
