import logging

from django.contrib.auth.backends import ModelBackend

from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.person import PersonContact
from pycorpkit.common.utils.constants import PHONE_NUMBER


LOGGER = logging.getLogger(__name__)


class PhoneModelBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        if phone is None:
            return None

        try:
            contact = PersonContact.objects.get(
                contact_type=PHONE_NUMBER,
                contact_value=phone,
                is_primary=True
            )
            user = User.objects.get(user_profile__person=contact.person)
            if user.check_password(password):
                return user
        except (PersonContact.DoesNotExist, User.DoesNotExist) as ex:
            LOGGER.error(f"PhoneModelBackend: error {ex}")
            return None
