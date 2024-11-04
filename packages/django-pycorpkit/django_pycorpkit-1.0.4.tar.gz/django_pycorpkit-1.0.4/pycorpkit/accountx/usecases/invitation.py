from datetime import timedelta

import jwt
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from pycorpkit.accountx.models.invitation import Invitation
from pycorpkit.common.utils.conf import SETTINGS
from pycorpkit.common.utils.email import send_email_asynchronously


@transaction.atomic
def invite_new_user(**user_to_invite):
    email = user_to_invite.get("email")
    role = user_to_invite.get("role")
    department = user_to_invite.get("department")
    organisation = user_to_invite.get("organisation")
    profile = user_to_invite.get("profile")

    payload = {
        "email": email,
        "department_id": str(department.pk),
        "role_id": str(role.pk),
        "profile_id": str(profile.pk),
        "exp": timezone.now() + timedelta(days=SETTINGS["INVITE_CODE_DAYS_EXPIRY"]),
    }
    invite_token = jwt.encode(payload, SETTINGS["SECRET_KEY"], algorithm="HS256")
    invitation, _ = Invitation.objects.update_or_create(
        email=email,
        defaults={
            "organisation": organisation,
        },
    )

    msg_subject = f"New User Invite For {organisation.name}"
    context = {
        "invite_url": f"{SETTINGS["CLIENT_DOMAIN"]}/invite/{invite_token}",
        "organisation_name": organisation.name,
    }
    html_message = render_to_string(SETTINGS["USER_INVITE_HTML_PATH"], context)
    plain_message = render_to_string(SETTINGS["USER_INVITE_TEXT_PATH"])
    send_email_asynchronously.delay(
        subject=msg_subject,
        plain_text=plain_message,
        html_message=html_message,
        recipients=[email],
    )
    invitation.invitation_sent = True
    invitation.save()
    return invite_token
