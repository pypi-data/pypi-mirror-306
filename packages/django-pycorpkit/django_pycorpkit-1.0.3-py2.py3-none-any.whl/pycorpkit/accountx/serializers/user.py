from pycorpkit.accountx.models.user import User
from pycorpkit.common.serializers.common import BaseModelSerializer
from pycorpkit.common.serializers.profile import (
    ContactSerializer,
    PersonResponseSerializer,
    UserProfileSerializer,
)


class UserSerializer(BaseModelSerializer):
    person = PersonResponseSerializer()
    profiles = UserProfileSerializer(many=True)
    contacts = ContactSerializer(many=True)

    class Meta:
        model = User
        exclude = [
            "created",
            "updated",
            "active",
            "created_by",
            "updated_by",
            "verify_code_expire",
            "is_verified",
            "change_pass_at_next_login",
            "is_system_user",
            "verify_code",
            "is_active",
        ]
