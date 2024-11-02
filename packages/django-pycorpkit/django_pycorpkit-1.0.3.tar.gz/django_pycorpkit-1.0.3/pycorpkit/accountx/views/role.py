from pycorpkit.accountx.filters.roles import (
    RoleFilter,
    RolePermissionFilter,
    UserRoleFilter,
)
from pycorpkit.accountx.models.permission import Permissions
from pycorpkit.accountx.models.role import Role, RolePermission, UserRole
from pycorpkit.accountx.serializers.roles import (
    PermissionsSerializer,
    RolePermissionSerializer,
    RoleSerializer,
    UserRoleSerializer,
)
from pycorpkit.common.utils.helpers import PERMS
from pycorpkit.common.views.base import BaseViewSet


class RoleViewSet(BaseViewSet):
    """
    Adds ability to add, update and returns roles.
    """

    permissions = {
        "GET": [PERMS.ROLE_VIEW],
        "POST": [PERMS.ROLE_CREATE],
        "PATCH": [PERMS.ROLE_EDIT],
        "DELETE": [PERMS.ROLE_DELETE],
    }
    queryset = Role.objects.filter(active=True).order_by("name").all()
    serializer_class = RoleSerializer
    filterset_class = RoleFilter
    http_method_names = ["get", "post", "patch", "delete"]


class RolePermissionViewSet(BaseViewSet):
    """
    Used to update and assign permissions directly to roles.
    """

    permissions = {
        "POST": [PERMS.ROLE_CREATE],
        "PATCH": [PERMS.ROLE_EDIT],
        "DELETE": [PERMS.ROLE_DELETE],
    }
    queryset = RolePermission.objects.filter(active=True).all()
    serializer_class = RolePermissionSerializer
    filterset_class = RolePermissionFilter
    http_method_names = ["post", "patch"]


class UserRoleViewSet(BaseViewSet):
    """
    Used to update and assign users to roles.
    """

    permissions = {
        "POST": [PERMS.ROLE_CREATE],
        "PATCH": [PERMS.ROLE_EDIT],
        "DELETE": [PERMS.ROLE_DELETE],
    }
    queryset = UserRole.objects.filter(active=True).all()
    serializer_class = UserRoleSerializer
    filterset_class = UserRoleFilter
    http_method_names = ["post", "patch"]


class PermissionsViewSet(BaseViewSet):
    """User to return all permissions."""

    queryset = Permissions.objects.filter(active=True).order_by("name").all()
    serializer_class = PermissionsSerializer
    permissions = {
        "GET": [PERMS.PERMISSION_VIEW],
        "POST": [PERMS.PROFILE_CREATE],
        "PATCH": [PERMS.PROFILE_EDIT],
        "DELETE": [PERMS.PROFILE_DELETE],
    }
    filterset_fields = ("name",)
    http_method_names = ("get",)
