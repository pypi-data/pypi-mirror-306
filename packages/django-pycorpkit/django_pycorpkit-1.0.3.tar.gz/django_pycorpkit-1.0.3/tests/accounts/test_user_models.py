from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from pycorpkit.accountx.models.user import (
    ExpiredVerificationCodeError,
    InvalidVerificationCodeError,
)

from pycorpkit.accountx.permissions.setup import PERM_NODE
from tests.helpers import (
    assertListEqual,
    create_test_department,
    create_test_department_member,
    create_test_organisation,
    create_test_permission,
    create_test_person,
    create_test_role,
    create_test_user_profile,
    create_test_user_role,
)

UserModel = get_user_model()


USER_VIEW = PERM_NODE("user_list", "View users", is_system_level=True)

USER_CREATE = PERM_NODE("user_create", "Create users", is_system_level=True)

USER_EDIT = PERM_NODE("user_edit", "Edit users", is_system_level=True)

USER_DELETE = PERM_NODE("user_delete", "Delete users", is_system_level=True)


def add_user_in_test_to_org(user):
    organisation = create_test_organisation()
    roles = ["Admin", "Super Admin"]
    role1 = create_test_role(roles[0], organisation)
    role2 = create_test_role(roles[1], organisation)

    perms = [USER_EDIT.name, USER_CREATE.name, USER_DELETE.name, USER_VIEW.name]
    for perm in perms:
        create_test_permission(perm, role1)

    person = create_test_person()
    department = create_test_department("Plumber Department", organisation)
    user_profile = create_test_user_profile(user, person)
    # Assign user to both roles
    for role in [role1, role2]:
        create_test_user_role(role=role, user_profile=user_profile)
    # add userprofile to a department/organisation
    create_test_department_member(user_profile, department)
    return organisation


class TestUserModel(TestCase):
    def test_bool_defaults(self):
        from model_bakery import baker
        user = baker.make(UserModel)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        self.assertFalse(user.agreed_to_terms)
        self.assertFalse(user.is_system_user)

    def test_has_permissions(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        perms = user.permission_names
        self.assertEqual(perms, {})

        organisation = add_user_in_test_to_org(user)

        user = UserModel.objects.get(pk=user.id)
        self.assertTrue(user.has_permissions([USER_VIEW.name], organisation.id))
        self.assertTrue(user.has_permissions([USER_CREATE.name], organisation.id))
        self.assertTrue(user.has_permissions([USER_EDIT.name], organisation.id))
        self.assertTrue(
            user.has_permissions([USER_VIEW.name, USER_CREATE.name], organisation.id)
        )
        self.assertTrue(
            user.has_permissions([USER_CREATE.name, USER_EDIT.name], organisation.id)
        )
        self.assertTrue(
            user.has_permissions(
                [USER_EDIT.name, USER_CREATE.name, USER_VIEW.name], organisation.id
            )
        )

    def test_permission_names(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        perms = user.permission_names
        self.assertEqual(perms, {})

        organisation = add_user_in_test_to_org(user)

        assertListEqual(
            user.permission_names.get(organisation.id),
            [
                USER_VIEW.name,
                USER_CREATE.name,
                USER_EDIT.name,
                USER_DELETE.name,
            ],
        )

    def test_role_names(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        roles = user.role_names
        self.assertEqual(len(roles), 0)

        organisation = add_user_in_test_to_org(user)

        roles = user.role_names.get(organisation.id)
        assertListEqual(roles, ["Super Admin", "Admin"])

    def test_generate_verify_code(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        assert not user.verify_code
        assert not user.verify_code_expire
        updated_user = UserModel.objects.generate_verify_code(user.email)
        assert updated_user.verify_code
        assert updated_user.verify_code_expire

    def test_generate_verify_code_email_address_not_found(self):
        with self.assertRaises(InvalidVerificationCodeError) as ex:
            non_existent_email = "idont_exist@gmail.com"
            UserModel.objects.generate_verify_code(non_existent_email)
        self.assertEqual("We can't find that email address, sorry!", str(ex.exception))

    def test_make_user_active(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        assert not user.is_active
        assert not user.verify_code
        assert not user.verify_code_expire
        updated_user = UserModel.objects.generate_verify_code(user.email)
        assert updated_user.verify_code
        assert updated_user.verify_code_expire
        updated_user = UserModel.objects.make_user_active(
            updated_user.email, updated_user.verify_code
        )
        user.refresh_from_db()
        assert not user.verify_code
        assert not user.verify_code_expire
        assert user.is_active

    def test_make_user_active_user_does_not_exist(self):
        with self.assertRaises(InvalidVerificationCodeError) as ex:
            non_existent_email = "kama@gmail.com"
            UserModel.objects.make_user_active(non_existent_email, 125789)
        self.assertEqual("User does not exist.", str(ex.exception))

    def test_make_user_active_invalid_verification_code(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        with self.assertRaises(InvalidVerificationCodeError) as ex:
            invalid_verify_code = 125
            UserModel.objects.make_user_active(user.email, invalid_verify_code)
        self.assertEqual("Verification code is invalid.", str(ex.exception))

    def test_make_user_active_expired_verification_code(self):
        from model_bakery import baker
        user = baker.make(UserModel, email="email@umoja.com")
        updated_user = UserModel.objects.generate_verify_code(user.email)
        assert updated_user.verify_code
        assert updated_user.verify_code_expire

        with self.assertRaises(ExpiredVerificationCodeError) as ex:
            updated_user.verify_code_expire = timezone.now() - timedelta(days=6)
            updated_user.save()
            UserModel.objects.make_user_active(
                updated_user.email, updated_user.verify_code
            )
        self.assertEqual("Verification code is expired.", str(ex.exception))
