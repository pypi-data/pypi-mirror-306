from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from pycorpkit.common.models.abstract import AbstractBase
from pycorpkit.common.models.attachment import Attachments
from pycorpkit.common.models.person import Person
from pycorpkit.common.utils.conf import SETTINGS


class UserProfile(AbstractBase):
    """This allows us to connect a user with a person."""

    user = models.ForeignKey(
        SETTINGS["AUTH_USER_MODEL"],
        on_delete=models.PROTECT,
        related_name="user_profile",
    )
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    is_organisation = models.BooleanField(default=False)
    search_vector = SearchVectorField(null=True)
    organisation = None

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]


class UserProfileAttachment(AbstractBase):
    """
    This makes it possible to associate
    files with users.
    """

    profile = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="user_profile_attachments"
    )
    attachment = models.ForeignKey(
        Attachments,
        null=True,
        blank=True,
        related_name="attachments_profiles",
        on_delete=models.PROTECT,
    )
    organisation = None
