from django.db import models
from django.utils.translation import gettext_lazy as _

from pycorpkit.accountx.models.permission import Permissions
from pycorpkit.common.models.abstract import AbstractBase
from pycorpkit.common.models.profile import UserProfile


class RoleTypes(models.TextChoices):
    SYSTEM = ("SYSTEM", _("System"))
    CUSTOM = ("CUSTOM", _("Custom"))


class Role(AbstractBase):
    """
    This model maintains a flat structure for roles at the data layer.
    Uses a simpler hierarchical representation at the application layer to
    determine access levels.
    A user can be assigned to one or more roles;
    the roles then group together granular permissions.
    """

    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    role_type = models.CharField(
        choices=RoleTypes.choices, max_length=16, default=RoleTypes.SYSTEM
    )

    class Meta(AbstractBase.Meta):
        unique_together = ("name", "organisation")

    @property
    def users(self):
        from pycorpkit.common.models.person import Person

        user_profiles = UserRole.objects.filter(role=self).values_list(
            "user_profile", flat=True
        )
        persons = Person.objects.filter(userprofile__in=user_profiles)
        return persons

    @property
    def permissions(self):
        role_perms = self.role_permissions.all()
        return [rp.permission for rp in role_perms]


class RolePermission(AbstractBase):
    """
    This model connects or defines a role and its permissions.
    Helps to assign permissions directly to roles.
    """

    role = models.ForeignKey(
        Role, related_name="role_permissions", on_delete=models.PROTECT
    )
    permission = models.ForeignKey(Permissions, on_delete=models.PROTECT)

    class Meta(AbstractBase.Meta):
        unique_together = (
            "role",
            "permission",
            "organisation",
        )


class UserRole(AbstractBase):
    """
    The UserRole model is linked to a UserProfile instead of directly to a User.
    This design choice likely reflects the intention to associate roles and
    permissions with the user's profile within a specific organization,
    rather than directly with the user across all organizations.

    Helps to assign roles to users based on their organizational context
    (e.g., organization-wide roles, branch-specific roles, department-specific roles).

    Rationale:
    1. Organization Context: The roles become organization-specific.
       This allows for granular control over user permissions within each organization
       they are a part of. Users may have different roles and permissions in
       different organizations, so linking the role to the profile within each
       organization captures this context effectively.

    2. Separation of Concerns: Keeping the role assignment at the profile level rather
       than the user level helps maintain separation of concerns.
       The UserProfile model serves as a bridge between the User and the specific
       organization they are associated with.
       This separation allows for clearer organization-specific management of
       roles and permissions.

    3. Flexibility: Linking UserRole to UserProfile provides flexibility in case
       the application needs to support scenarios where a user may have different
       roles within the same organization based on different
       profiles (e.g., if a user holds different positions
       within different departments of the same organization).

    4. Scalability: Each organization can define its own
       set of roles and permissions tailored to its specific needs,
       managed within the context of user profiles.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="user_roles"
    )
    role = models.ForeignKey(Role, related_name="role_users", on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            "user_profile",
            "role",
        )
