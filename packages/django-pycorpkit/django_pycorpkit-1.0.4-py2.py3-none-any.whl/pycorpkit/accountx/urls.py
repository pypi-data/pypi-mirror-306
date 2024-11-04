from django_rest_passwordreset.views import (
    ResetPasswordConfirmViewSet,
    ResetPasswordRequestTokenViewSet,
)
from rest_framework.routers import DefaultRouter

from pycorpkit.accountx.views.change_password import ChangePasswordViewSet
from pycorpkit.accountx.views.invitation import (
    InvitationAcceptViewSet,
    InvitationViewSet,
)
from pycorpkit.accountx.views.login import LoginViewSet
from pycorpkit.accountx.views.register import (
    ActivateUserViewSet,
    RegisterUserViewSet,
    ResendActivationEmailViewSet,
)
from pycorpkit.accountx.views.role import (
    PermissionsViewSet,
    RolePermissionViewSet,
    RoleViewSet,
    UserRoleViewSet,
)
from pycorpkit.accountx.views.user import UserViewSet

user_router = DefaultRouter()
user_router.register(r"users", UserViewSet)
user_router.register(r"register", RegisterUserViewSet, basename="register")
user_router.register(r"activate", ActivateUserViewSet, basename="user_activate")
user_router.register(r"login", LoginViewSet, basename="login")
user_router.register(
    r"resend-verify-code", ResendActivationEmailViewSet, basename="resend-verify-code"
)
user_router.register(
    r"change-password", ChangePasswordViewSet, basename="change-password"
)

password_router = DefaultRouter()
password_router.register(
    r"forgot_password", ResetPasswordRequestTokenViewSet, basename="forgot_password"
)
password_router.register(
    r"confirm_password", ResetPasswordConfirmViewSet, basename="reset_password"
)

permission_router = DefaultRouter()
permission_router.register(r"permission", PermissionsViewSet)
permission_router.register(r"role-permissions", RolePermissionViewSet)

roles_router = DefaultRouter()
roles_router.register(r"role", RoleViewSet)
roles_router.register(r"user-roles", UserRoleViewSet)

invitations_router = DefaultRouter()
invitations_router.register(r"invite", InvitationViewSet)
invitations_router.register(r"accept", InvitationAcceptViewSet, basename="accept")
