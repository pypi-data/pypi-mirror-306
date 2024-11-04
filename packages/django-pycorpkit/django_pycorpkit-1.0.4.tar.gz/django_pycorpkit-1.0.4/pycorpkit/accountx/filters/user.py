from pycorpkit.accountx.models.invitation import Invitation
from pycorpkit.accountx.models.user import User
from pycorpkit.common.filters.base import BaseFilter


class UserFilter(BaseFilter):

    class Meta:
        model = User
        fields = ["id", "email", "is_active"]


class UserInviteFilter(BaseFilter):

    class Meta:
        model = Invitation
        fields = "__all__"
