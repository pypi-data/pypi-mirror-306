import logging
import uuid

import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

from pycorpkit.common.models.organisation import Organisation
from pycorpkit.common.utils.constants import CONTACT_TYPES, EMAIL, PHONE_NUMBER

LOGGER = logging.getLogger(__file__)


class AbstractBase(models.Model):
    """Base class for most models in the application."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, null=False)
    created_by = models.UUIDField(blank=True, null=True)
    updated = models.DateTimeField(default=timezone.now)
    updated_by = models.UUIDField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",
    )

    organisation_verify = []

    class Meta:
        abstract = True
        ordering = ("-updated", "-created")


class Contact(AbstractBase):
    """A common abstract model for all contacts"""

    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPES)
    contact_value = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    organisation = None

    model_validators = [
        "validate_phone_number_is_valid",
        "validate_email_address",
    ]

    @property
    def is_phone_number(self):
        return self.contact_type == PHONE_NUMBER

    @property
    def is_email_address(self):
        return self.contact_type == EMAIL

    def validate_phone_number_is_valid(self):
        """Ensure that only valid phone numbers are saved."""
        error_msg = {"contact": "Enter a valid phone number."}
        phne = to_python(self.contact)
        if not phonenumbers.is_valid_number(phne) and self.is_phone_number:
            LOGGER.error("Invalid phone number: {} -> {}".format(self.contact, phne))
            raise ValidationError(error_msg)

    def validate_email_address(self):
        """Email address should be in the form address@domain.top_level."""
        if self.is_email_address:
            try:
                validate_email(self.contact)
            except ValidationError as e:
                raise ValidationError({"contact": e})

    class Meta:
        ordering = ("-updated", "-created")
        abstract = True


class AbstractOrgDetails(AbstractBase):
    """
    A common model of organisation details.
    """

    email_address = models.EmailField(max_length=50, blank=True)
    phone_number = PhoneNumberField(blank=True)
    physical_address = models.TextField(blank=True)
    postal_address = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True
