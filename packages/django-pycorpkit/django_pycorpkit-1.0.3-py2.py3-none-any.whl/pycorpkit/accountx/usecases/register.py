from http import HTTPStatus

from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.person import Person, PersonContact
from pycorpkit.common.models.profile import UserProfile
from pycorpkit.common.utils.conf import SETTINGS
from pycorpkit.common.utils.constants import PHONE_NUMBER
from pycorpkit.common.utils.email import send_email_asynchronously


def create_user(registration_data):
    email = registration_data["email"]
    password = registration_data["password"]
    userdata = {"username": email}
    user = User.objects.create_user(email=email, password=password, **userdata)
    new_user = User.objects.generate_verify_code(user.email)
    return new_user, email


def create_person(registration_data):
    email = registration_data["email"]
    first_name = registration_data.get("first_name")
    last_name = registration_data.get("last_name")
    if not first_name and not last_name:
        first_name = email
        last_name = email

    return Person.objects.create(
        first_name=first_name,
        last_name=last_name,
    )


@transaction.atomic
def create_profile(user, person):
    profile_defaults = {
        "user": user,
        "person": person,
    }

    profile = UserProfile.objects.create(**profile_defaults)
    return profile


def send_user_activation_email(user):
    print(f"verification code: {user.verify_code}")
    expiration_hours = round(
        (user.verify_code_expire - timezone.now()).total_seconds() / 3600
    )

    app_name = SETTINGS["APP_NAME"]
    msg_subject = f"Activate Your {app_name} Account"
    context = {
        "full_name": user.person.first_name,
        "verification_code": user.verify_code,
        "verify_code_expire": expiration_hours,
        "app_name": app_name,
    }
    html_message = render_to_string(SETTINGS["USER_ACTIVATE_HTML_PATH"], context)
    plain_message = render_to_string(SETTINGS["USER_ACTIVATE_TEXT_PATH"])
    send_email_asynchronously.delay(
        subject=msg_subject,
        plain_text=plain_message,
        html_message=html_message,
        recipients=[user.email],
    )


@transaction.atomic
def register_user(registration_data):
    user, _ = create_user(registration_data)
    person = create_person(registration_data)
    phone = registration_data.get("phone")
    if phone:
        PersonContact.objects.create(
            person=person,
            contact_value=phone,
            contact_type=PHONE_NUMBER
        )
    create_profile(user, person)
    send_user_activation_email(user)
    response_data = {"user_id": user.id}
    return response_data, HTTPStatus.CREATED
