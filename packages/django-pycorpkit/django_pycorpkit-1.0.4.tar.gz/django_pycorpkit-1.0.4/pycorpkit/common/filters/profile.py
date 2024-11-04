import django_filters

from pycorpkit.common.filters.base import BaseFilter
from pycorpkit.common.models.person import Person
from pycorpkit.common.models.profile import UserProfile, UserProfileAttachment


class UserProfileFilter(BaseFilter):
    user_id = django_filters.CharFilter("user__id")
    person_id = django_filters.UUIDFilter("person__id")

    class Meta:
        model = UserProfile
        fields = ("user", "person")


class UserProfileAttachmentFilter(BaseFilter):
    user_id = django_filters.CharFilter("profile__user__id")

    class Meta:
        model = UserProfileAttachment
        fields = (
            "profile",
            "attachment",
            "created",
            "updated",
        )


class PersonFilter(BaseFilter):
    class Meta:
        model = Person
        fields = ("first_name", "last_name", "id_number", "surname")
