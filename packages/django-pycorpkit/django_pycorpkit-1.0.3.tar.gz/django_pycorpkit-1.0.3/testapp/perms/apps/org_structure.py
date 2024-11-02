from testapp.perms.apps.setup import PERM_NODE

ORGANISATION_VIEW = PERM_NODE(
    "organisation_list",
    "View organisations",
    is_deprecated=False,
    is_system_level=True,
)

ORGANISATION_CREATE = PERM_NODE(
    "organisation_create",
    "Create organisations",
    is_deprecated=False,
    is_system_level=True,
)

ORGANISATION_EDIT = PERM_NODE(
    "organisation_edit",
    "Edit organisations",
    is_deprecated=False,
    is_system_level=True,
)

ORGANISATION_DELETE = PERM_NODE(
    "organisation_delete",
    "Remove organisations",
    is_deprecated=False,
    is_system_level=True,
)

ORGANISATION_MANAGE = PERM_NODE(
    "organisation_manage",
    "Manage organisations",
    is_system_level=True,
    children=(ORGANISATION_CREATE, ORGANISATION_EDIT, ORGANISATION_VIEW),
)

BRANCH_VIEW = PERM_NODE(
    "branch_list",
    "View branches",
    is_system_level=True,
)

BRANCH_CREATE = PERM_NODE(
    "branch_create",
    "Create branches",
    is_system_level=True,
)

BRANCH_EDIT = PERM_NODE(
    "branch_edit",
    "Edit branches",
    is_system_level=True,
)

BRANCH_DELETE = PERM_NODE("branch_delete", "Delete branches")

BRANCH_MANAGE = PERM_NODE(
    "branch_manage",
    "Manage branches",
    children=(BRANCH_VIEW, BRANCH_CREATE, BRANCH_EDIT),
)

DEPARTMENT_VIEW = PERM_NODE("department_list", "View departments", is_system_level=True)

DEPARTMENT_CREATE = PERM_NODE(
    "department_create",
    "Create departments",
    is_system_level=True,
)

DEPARTMENT_EDIT = PERM_NODE(
    "department_edit",
    "Edit departments",
    is_system_level=True,
)

DEPARTMENT_DELETE = PERM_NODE("department_delete", "Delete departments")

DEPARTMENT_MANAGE = PERM_NODE(
    "department_manage",
    "Manage departments",
    children=(
        DEPARTMENT_VIEW,
        DEPARTMENT_CREATE,
        DEPARTMENT_EDIT,
    ),
)
