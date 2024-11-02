from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from pycorpkit.accountx.models.invitation import Invitation
from pycorpkit.accountx.models.role import Role
from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.profile import UserProfile
from pycorpkit.common.serializers.common import BaseModelSerializer
from pycorpkit.common.utils.error_codes import ErrorCodes
from pycorpkit.org_structure.models.department import Department


class UserToInviteInput(serializers.Serializer):
    email = serializers.EmailField(max_length=100, allow_blank=False)
    role = PrimaryKeyRelatedField(queryset=Role.objects.all())
    profile = PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    department = PrimaryKeyRelatedField(queryset=Department.objects.all())

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError(ErrorCodes.USER_SIGNUP_NEEDED.value)
        for department in user.departments:
            if department.id == data["department"].id:
                raise serializers.ValidationError(
                    ErrorCodes.USER_ALREADY_A_MEMBER.value
                )
        profile = data["profile"]
        if profile.id not in user.profiles.all().values_list("id", flat=True):
            raise serializers.ValidationError(ErrorCodes.PROFILE_MISMATCH.value)
        return data


class AcceptInviteInput(serializers.Serializer):
    token = serializers.CharField(max_length=450, allow_blank=False)


class InvitationSerializer(BaseModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"
