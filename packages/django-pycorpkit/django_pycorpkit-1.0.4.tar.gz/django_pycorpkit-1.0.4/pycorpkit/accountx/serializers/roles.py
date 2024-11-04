from rest_framework import serializers

from pycorpkit.accountx.models.permission import Permissions
from pycorpkit.accountx.models.role import Role, RolePermission, UserRole
from pycorpkit.common.serializers.common import BaseModelSerializer


class RoleSerializer(BaseModelSerializer):
    users = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "role_type",
            "organisation",
            "users",
            "permissions",
            "created",
        ]

    def get_users(self, obj) -> list:
        return list(set(user.full_name for user in obj.users))

    def get_permissions(self, obj) -> list:
        return [perm.name for perm in obj.permissions]


class RolePermissionSerializer(BaseModelSerializer):
    class Meta:
        model = RolePermission
        fields = (
            "id",
            "role",
            "permission",
            "organisation",
        )


class UserRoleSerializer(BaseModelSerializer):
    class Meta:
        model = UserRole
        fields = (
            "id",
            "role",
            "user_profile",
            "organisation",
        )


class PermissionsSerializer(BaseModelSerializer):
    class Meta:
        model = Permissions
        fields = ["id", "name", "description", "created"]
