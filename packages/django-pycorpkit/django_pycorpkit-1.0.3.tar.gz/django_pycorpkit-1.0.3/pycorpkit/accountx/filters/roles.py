from django_filters import rest_framework as filters

from pycorpkit.accountx.models.role import Role, RolePermission, RoleTypes, UserRole
from pycorpkit.common.filters.base import BaseFilter


class RoleFilter(BaseFilter):
    name = filters.CharFilter(lookup_expr="iexact")
    role_type = filters.ChoiceFilter(choices=RoleTypes.choices)

    class Meta:
        model = Role
        fields = ["name", "role_type"]


class RolePermissionFilter(BaseFilter):
    role = filters.NumberFilter(field_name="role__id")
    permission = filters.NumberFilter(field_name="permission__id")

    class Meta:
        model = RolePermission
        fields = ["role", "permission"]


class UserRoleFilter(BaseFilter):
    user_profile = filters.NumberFilter(field_name="user_profile__id")
    role = filters.NumberFilter(field_name="role__id")

    class Meta:
        model = UserRole
        fields = ["user_profile", "role"]
