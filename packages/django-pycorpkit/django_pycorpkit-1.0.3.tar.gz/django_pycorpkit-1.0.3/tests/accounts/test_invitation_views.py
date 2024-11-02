from unittest.mock import patch

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from pycorpkit.accountx.models.invitation import Invitation
from pycorpkit.accountx.models.role import UserRole
from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.person import Person
from pycorpkit.common.models.profile import UserProfile
from pycorpkit.common.utils.error_codes import ErrorCodes
from pycorpkit.org_structure.models.department import DepartmentMembers


class TestInviteUserViews:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, client, role, user_profile, department):
        self.client = client
        self.role = role
        self.profile = user_profile
        self.department = department
        self.url = reverse("v1:invitation-invite-user")

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "invite_create"}], indirect=True
    )
    @patch("pycorpkit.accountx.usecases.invitation.send_email_asynchronously")
    def test_can_invite_user_successfully(self, mock_email, assign_permission):
        assert Invitation.objects.count() == 0
        person = baker.make(Person, first_name="Omosh", last_name="Kame")
        user = baker.make(User, email="omosh@gmail.com")
        profile = baker.make(UserProfile, user=user, person=person)
        data = {
            "email": profile.user.email,
            "role": self.role.id,
            "department": self.department.id,
            "profile": profile.id,
        }
        response = self.client.post(self.url, data)
        mock_email.delay.assert_called_once()
        assert response.status_code == status.HTTP_200_OK
        assert Invitation.objects.count() == 1
        invitation = Invitation.objects.first()
        assert invitation.invitation_sent

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "invite_create"}], indirect=True
    )
    @patch("pycorpkit.accountx.usecases.invitation.send_email_asynchronously")
    def test_when_the_profile_used_is_not_attached_to_the_user(
        self, mock_email, assign_permission
    ):
        assert Invitation.objects.count() == 0
        person = baker.make(Person, first_name="Omosh", last_name="Kame")
        user = baker.make(User, email="omosh@gmail.com")
        profile = baker.make(UserProfile, person=person)
        data = {
            "email": user.email,
            "role": self.role.id,
            "department": self.department.id,
            "profile": profile.id,
        }
        response = self.client.post(self.url, data)
        assert (
            response.data["detail"] == f"non_field_errors: {ErrorCodes.PROFILE_MISMATCH.value}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Invitation.objects.count() == 0
        mock_email.delay.assert_not_called()

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "invite_create"}], indirect=True
    )
    def test_user_invite_when_email_is_not_supplied(self, assign_permission):
        data = {
            "role": self.role.id,
            "department": self.department.id,
            "profile": self.profile.id,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "email: This field is required."

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "invite_create"}], indirect=True
    )
    @patch("pycorpkit.accountx.usecases.invitation.send_email_asynchronously")
    def test_user_invite_when_user_has_not_signed_up(
        self, mock_email, assign_permission
    ):
        assert Invitation.objects.count() == 0
        data = {
            "email": "ihavenotsignedup@gmail.com",
            "role": self.role.id,
            "department": self.department.id,
            "profile": self.profile.id,
        }
        response = self.client.post(self.url, data)
        assert (
            response.data["detail"] == f"non_field_errors: {ErrorCodes.USER_SIGNUP_NEEDED.value}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Invitation.objects.count() == 0
        mock_email.delay.assert_not_called()

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "invite_create"}], indirect=True
    )
    @patch("pycorpkit.accountx.usecases.invitation.send_email_asynchronously")
    def test_user_invite_when_who_is_already_in_that_department(
        self, mock_email, assign_permission
    ):
        assert Invitation.objects.count() == 0
        url = reverse("v1:invitation-invite-user")
        data = {
            "email": self.profile.user.email,
            "role": self.role.id,
            "department": self.department.id,
            "profile": self.profile.id,
        }
        response = self.client.post(url, data)
        assert (
            response.data["detail"] == f"non_field_errors: {ErrorCodes.USER_ALREADY_A_MEMBER.value}" # noqa
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Invitation.objects.count() == 0
        mock_email.delay.assert_not_called()


class TestAcceptInviteViews:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, client, role, user_profile, department):
        self.client = client
        self.role = role
        self.profile = user_profile
        self.department = department
        self.url = reverse("v1:accept-accept-invite")

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "invite_create"}], indirect=True
    )
    @patch("pycorpkit.accountx.usecases.invitation.send_email_asynchronously")
    def test_can_accept_user_invite_successfully(self, mock_email, assign_permission):
        assert Invitation.objects.count() == 0
        person = baker.make(Person, first_name="Omosh", last_name="Kame")
        user = baker.make(User, email="omosh@gmail.com")
        profile = baker.make(UserProfile, user=user, person=person)
        data = {
            "email": profile.user.email,
            "role": self.role.id,
            "department": self.department.id,
            "profile": profile.id,
        }
        url = reverse("v1:invitation-invite-user")
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert Invitation.objects.count() == 1
        invitation = Invitation.objects.first()
        assert invitation.invitation_sent
        mock_email.delay.assert_called_once()
        # Now we can invite the user using the
        # token obtained from the above invite.
        data = {"token": response.data["token"]}
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert DepartmentMembers.objects.filter(user=self.profile).count() == 1
        email = DepartmentMembers.objects.get(user=self.profile).user.user.email
        assert email == self.profile.user.email
        assert UserRole.objects.filter(user_profile=self.profile).count() == 1
        assert (
            UserRole.objects.get(user_profile=self.profile).user_profile == self.profile
        )

    def test_when_token_is_not_supplied_then_request_does_not_succceed(self):
        data = {
            "invalid": "kksksks",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "token: This field is required."

    def test_when_the_token_is_not_valid_then_error_is_returned(self):
        data = {
            "token": "thisisinvalid",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The invitation token is invalid"
