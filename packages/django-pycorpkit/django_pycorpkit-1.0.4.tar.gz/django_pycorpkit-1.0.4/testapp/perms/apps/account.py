from testapp.perms.apps.setup import PERM_NODE

PERMISSION_VIEW = PERM_NODE("permission_list", "View permissions", is_system_level=True)
PERMISSION_CREATE = PERM_NODE(
    "permission_create", "Create permissions", is_system_level=True
)
PERMISSION_EDIT = PERM_NODE("permission_edit", "Edit permissions", is_system_level=True)
PERMISSION_DELETE = PERM_NODE(
    "permission_delete", "Delete permissions", is_system_level=True
)
PERMISSION_MANAGE = PERM_NODE(
    "permission_manage",
    "Create, Edit and View permissions",
    is_system_level=True,
    children=(
        PERMISSION_VIEW,
        PERMISSION_CREATE,
        PERMISSION_EDIT,
    ),
)

ROLE_VIEW = PERM_NODE("role_list", "View roles")

ROLE_CREATE = PERM_NODE("role_create", "Create roles")

ROLE_EDIT = PERM_NODE("role_edit", "Edit roles")

ROLE_DELETE = PERM_NODE("role_delete", "Delete roles")

ROLE_MANAGE = PERM_NODE(
    "role_manage",
    "Create, Edit and View roles",
    children=(
        ROLE_VIEW,
        ROLE_CREATE,
        ROLE_EDIT,
    ),
)

USER_VIEW = PERM_NODE("user_list", "View users", is_system_level=True)

USER_CREATE = PERM_NODE("user_create", "Create users", is_system_level=True)

USER_EDIT = PERM_NODE("user_edit", "Edit users", is_system_level=True)

USER_DELETE = PERM_NODE("user_delete", "Delete users", is_system_level=True)

USER_MANAGE = PERM_NODE(
    "user_manage",
    "Create, Edit and View users",
    is_system_level=True,
    children=(
        USER_VIEW,
        USER_CREATE,
        USER_EDIT,
    ),
)


PROFILE_VIEW = PERM_NODE("profile_list", "View profiles")

PROFILE_CREATE = PERM_NODE("profile_create", "Create profiles")

PROFILE_EDIT = PERM_NODE("profile_edit", "Edit profiles")

PROFILE_DELETE = PERM_NODE(
    "profile_delete",
    "Delete profile",
    is_system_level=True,
)

PROFILE_MANAGE = PERM_NODE(
    "profile_manage",
    "Create, Edit and View profiles",
    children=(
        PROFILE_VIEW,
        PROFILE_CREATE,
        PROFILE_EDIT,
    ),
)

INVITE_VIEW = PERM_NODE("invite_list", "View user invites")
INVITE_CREATE = PERM_NODE("invite_create", "Create user invites")
INVITE_EDIT = PERM_NODE("invite_edit", "Edit user invites")
INVITE_DELETE = PERM_NODE("invite_delete", "Delete user invite")
INVITE_MANAGE = PERM_NODE(
    "invite_manage",
    "Create, Edit and View user invites",
    is_system_level=True,
    children=(
        INVITE_VIEW,
        INVITE_CREATE,
        INVITE_EDIT,
    ),
)
