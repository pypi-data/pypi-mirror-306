from unittest.mock import patch

import pytest
from django.conf import settings

from pycorpkit.accountx.models.permission import Permissions
from pycorpkit.accountx.models.role import Role, RolePermission, UserRole
from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.person import Person
from pycorpkit.common.models.profile import UserProfile
from pycorpkit.common.usecases.organisation import (
    add_permission_to_a_role,
    add_user_to_a_department,
    assign_a_role_to_a_user_profile,
    create_branch_and_department,
    create_organisation_user,
    create_permission_and_roles,
    create_person,
    create_user_and_profile,
    get_or_create_role,
    initialize_department,
    initialize_organisation,
    notify_organisation_of_activation,
    setup_default_roles_and_permissions,
)
from pycorpkit.common.utils.helpers import get_default_roles
from pycorpkit.org_structure.models.branch import Branch
from pycorpkit.org_structure.models.department import Department, DepartmentMembers
import testapp
from tests.helpers import create_test_organisation


def test_get_default_roles():
    roles = get_default_roles()
    all_roles = []
    for role, _ in roles.items():
        all_roles.append(role)

    assert len(all_roles) == 4
    assert "Branch Admin" in all_roles
    assert "Department Admin" in all_roles
    assert "Organisation Admin" in all_roles
    assert "User" in all_roles


def test_can_create_role(organisation):
    assert Role.objects.count() == 0
    name = "Doctor"
    role = get_or_create_role(name, organisation)
    assert role.name == name
    assert Role.objects.count() == 1


def test_can_add_user_to_a_department(department, user_profile):
    assert DepartmentMembers.objects.count() == 0
    add_user_to_a_department(department, user_profile)
    assert DepartmentMembers.objects.count() == 1


def test_can_create_branch_and_department(organisation):
    assert Branch.objects.count() == 0
    assert Department.objects.count() == 0
    department = create_branch_and_department(organisation)
    assert Branch.objects.count() == 1
    assert Department.objects.count() == 1
    assert department.name == "Main Department"
    assert department.branch.name == "Main Branch"


def test_can_add_permission_to_a_role(role):
    assert Permissions.objects.count() == 0
    assert RolePermission.objects.count() == 0
    add_permission_to_a_role(role, testapp.perms.apps.perm_groups.BRANCH_ADMIN[0])
    assert Permissions.objects.count() == 1
    assert RolePermission.objects.count() == 1
    add_permission_to_a_role(role, testapp.perms.apps.perm_groups.BRANCH_ADMIN[1])
    assert Permissions.objects.count() == 2
    assert RolePermission.objects.count() == 2


def test_create_permission_and_roles(role):
    assert Role.objects.count() == 1
    assert Permissions.objects.count() == 0
    assert RolePermission.objects.count() == 0
    create_permission_and_roles(role, testapp.perms.apps.perm_groups.ORGANISATION_ADMIN)
    assert RolePermission.objects.count() == 27
    assert Permissions.objects.count() == 27
    assert Role.objects.count() == 1


def test_assign_a_role_to_a_user_profile(role, user_profile):
    assert UserRole.objects.count() == 0
    assign_a_role_to_a_user_profile(role, user_profile)
    assert UserRole.objects.count() == 1


def test_create_organisation_user():
    assert User.objects.count() == 0
    user, _ = create_organisation_user("mwelusi@gmail.com")
    assert User.objects.count() == 1
    assert user.is_active


def test_create_person():
    assert Person.objects.count() == 0
    person = create_person("bonoko")
    assert Person.objects.count() == 1
    assert person.first_name == "bonoko"
    assert person.last_name == "bonoko"


@patch("pycorpkit.common.usecases.organisation.send_email_asynchronously")
def test_notify_organisation_of_activation(mock_email, organisation):
    notify_organisation_of_activation(
        organisation_name=organisation.name,
        email_address=organisation.email_address,
        password="pass",
    )
    html_message = f'<p>Dear Test Org Team,</p>\n\n<p>Welcome to {settings.APP_NAME}! We are excited to have you join us.</p>\n\n<p>To get started, please use the following temporary password to sign in to your account.</p>\n\n<p style="font-size: 1.5em; font-weight: bold;">pass</p>\n\n<p>We recommend changing your password after your first login for security purposes.</p>\n\n<p>If you encounter any issues or have any questions, please don\'t hesitate to contact our support.</p>\n\n<p>Best,</p>\n\n<p>The {settings.APP_NAME} Team</p>'  # noqa
    mock_email.delay.assert_called_with(
        subject=f"Your {settings.APP_NAME} Account Details",
        plain_text="Instructions for organisation account details",
        html_message=html_message,
        recipients=["org@gmail.com"],
    )


def test_create_user_and_profile(organisation):
    assert User.objects.count() == 0
    assert Person.objects.count() == 0
    assert UserProfile.objects.count() == 0
    create_user_and_profile(organisation)
    assert User.objects.count() == 1
    assert Person.objects.count() == 1
    assert UserProfile.objects.count() == 1


def test_initialize_department(organisation, user_profile):
    assert Branch.objects.count() == 0
    assert Department.objects.count() == 0
    assert DepartmentMembers.objects.count() == 0
    department = initialize_department(organisation, user_profile)
    assert Branch.objects.count() == 1
    assert Department.objects.count() == 1
    assert DepartmentMembers.objects.count() == 1
    assert department.name == "Main Department"
    assert department.branch.name == "Main Branch"


def test_setup_default_roles_and_permissions(organisation, user_profile):
    assert Role.objects.count() == 0
    assert Permissions.objects.count() == 0
    assert RolePermission.objects.count() == 0
    assert UserRole.objects.count() == 0
    roles_and_perms = get_default_roles().items()
    setup_default_roles_and_permissions(organisation, user_profile, roles_and_perms)
    assert Role.objects.count() == 4
    assert RolePermission.objects.count() == 51
    assert Permissions.objects.count() == 27
    assert UserRole.objects.count() == 4


@patch("pycorpkit.common.usecases.organisation.send_email_asynchronously")
def test_initialize_organisation(mock_email, organisation):
    assert Branch.objects.count() == 0
    assert Department.objects.count() == 0
    assert DepartmentMembers.objects.count() == 0
    assert Role.objects.count() == 0
    assert RolePermission.objects.count() == 0
    assert Permissions.objects.count() == 0
    assert UserRole.objects.count() == 0
    roles_and_perms = get_default_roles().items()
    initialize_organisation(organisation, roles_and_perms)
    assert Branch.objects.count() == 1
    assert Department.objects.count() == 1
    assert DepartmentMembers.objects.count() == 1
    assert Role.objects.count() == 4
    assert Permissions.objects.count() == 27
    assert RolePermission.objects.count() == 51
    assert UserRole.objects.count() == 4


@pytest.mark.enable_signals
@patch("pycorpkit.common.usecases.organisation.send_email_asynchronously")
def test_setup_organisation_signal(mock_email):
    organisation = create_test_organisation()
    assert Branch.objects.count() == 1
    assert Department.objects.count() == 1
    assert DepartmentMembers.objects.count() == 1
    assert Role.objects.count() == 4
    assert Permissions.objects.count() == 27
    assert RolePermission.objects.count() == 51
    assert UserRole.objects.count() == 4
    organisation.name = "Updated Organisation"
    organisation.save()
    mock_email.delay.assert_called_once()
