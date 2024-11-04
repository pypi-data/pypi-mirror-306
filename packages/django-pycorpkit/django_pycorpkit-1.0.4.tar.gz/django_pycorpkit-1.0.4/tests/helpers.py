import pytest

from model_bakery import baker

from pycorpkit.accountx import models as account_model
from pycorpkit.accountx.models.role import Role, RolePermission, UserRole
from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.organisation import Organisation, OrganisationStatuses
from pycorpkit.common.models.person import Person, PersonContact
from pycorpkit.common.models.profile import UserProfile
from pycorpkit.org_structure.models.branch import Branch
from pycorpkit.org_structure.models.department import Department, DepartmentMembers

pytestmark = pytest.mark.django_db


def create_test_organisation(name="Test Org", status=OrganisationStatuses.VERIFIED):
    return baker.make(
        Organisation,
        name=name,
        email_address="org@gmail.com",
        phone_number="+254721456789",
        status=status,
    )


def create_test_user(
    username="mail@mail.com", email="mail@mail.com", is_active=True, password="abc@123"
):
    user = User.objects.create(username=username, email=email, is_active=is_active)
    user.set_password(password)
    user.save()
    return user


def create_test_contact(person, contact_type, contact_value, is_primary):
    return baker.make(
        PersonContact,
        contact_type=contact_type,
        contact_value=contact_value,
        is_primary=is_primary,
        person=person,
    )


def create_test_person(first_name="John", last_name="Doe"):
    return baker.make(Person, first_name=first_name, last_name=last_name)


def create_test_role(name, organisation, description="Manage the org"):
    return baker.make(
        Role, name=name, organisation=organisation, description=description
    )


def create_test_user_profile(user, person):
    return baker.make(UserProfile, user=user, person=person)


def create_test_branch(name, organisation):
    return baker.make(Branch, name=name, organisation=organisation)


def create_test_department(name, organisation):
    return baker.make(Department, name=name, organisation=organisation)


def create_test_department_member(user_profile, department):
    return baker.make(
        DepartmentMembers,
        user=user_profile,
        organisation=department.organisation,
        department=department,
    )


def create_test_permission(name, role, children=[], description="perm desc"):
    if children:
        for child in children:
            perm_child = baker.make(account_model.Permissions, name=child, description=description)
            baker.make(
                RolePermission,
                role=role,
                permission=perm_child,
                organisation=role.organisation,
            )

    perm = baker.make(
       account_model.Permissions, name=name, description=description, children=children
    )
    baker.make(
        RolePermission, role=role, permission=perm, organisation=role.organisation
    )


def create_test_user_role(role, user_profile):
    return baker.make(
        UserRole, role=role, user_profile=user_profile, organisation=role.organisation
    )


def assertListEqual(a, b):
    assert len(a) == len(b) and sorted(a) == sorted(b)


def sorted_dict_values(d):
    return {k: sorted(v) for k, v in d.items()}
