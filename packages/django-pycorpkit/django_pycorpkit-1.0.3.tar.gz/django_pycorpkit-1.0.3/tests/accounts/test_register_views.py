from unittest.mock import patch

from pycorpkit.common.models.person import PersonContact
from pycorpkit.common.utils.constants import PHONE_NUMBER
import pytest
from django.conf import settings
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from pycorpkit.accountx.models.user import User
from pycorpkit.common.utils.error_codes import ErrorCodes

pytestmark = pytest.mark.django_db


class TestRegisterUserView:
    def setup_method(self):
        self.payload = {
            "email": "doe@gmail.com",
            "password": "pass@123",
        }
        self.url = reverse("v1:register-list")

    @patch("pycorpkit.accountx.usecases.register.send_email_asynchronously")
    def test_can_register_user_successfully(self, mock_email, unauthenticated_client):
        assert User.objects.count() == 0

        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=self.payload["email"])
        html_message = f'<p>Hi {self.payload["email"]},</p>\n\n<p>Thank you for signing up for {settings.APP_NAME}. Use the below code to verify your email:</p>\n\n<p style="font-size: 1.5em; font-weight: bold;">{user.verify_code}</p>\n\n<p>The verification code will expire in 72 hours. If you did not sign up for a {settings.APP_NAME} account, you can safely ignore this email.</p>\n\n<p>Best,</p>\n\n<p>{settings.APP_NAME} Team</p>'  # noqa
        mock_email.delay.assert_called_with(
            subject=f"Activate Your {settings.APP_NAME} Account",
            plain_text="Instructions to activate account",
            html_message=html_message,
            recipients=[self.payload["email"]],
        )
        assert User.objects.count() == 1
        assert PersonContact.objects.count() == 0

    @patch("pycorpkit.accountx.usecases.register.send_email_asynchronously")
    def test_can_register_user_successfully_with_phone(self, mock_email, unauthenticated_client):
        assert User.objects.count() == 0
        new_dict = {**self.payload, **{"phone": "0721456789"}}
        response = unauthenticated_client.post(self.url, new_dict)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=self.payload["email"])
        html_message = f'<p>Hi {self.payload["email"]},</p>\n\n<p>Thank you for signing up for {settings.APP_NAME}. Use the below code to verify your email:</p>\n\n<p style="font-size: 1.5em; font-weight: bold;">{user.verify_code}</p>\n\n<p>The verification code will expire in 72 hours. If you did not sign up for a {settings.APP_NAME} account, you can safely ignore this email.</p>\n\n<p>Best,</p>\n\n<p>{settings.APP_NAME} Team</p>'  # noqa
        mock_email.delay.assert_called_with(
            subject=f"Activate Your {settings.APP_NAME} Account",
            plain_text="Instructions to activate account",
            html_message=html_message,
            recipients=[self.payload["email"]],
        )
        assert User.objects.count() == 1
        assert PersonContact.objects.get(contact_value="0721456789", contact_type=PHONE_NUMBER)

    @patch("pycorpkit.accountx.usecases.register.send_email_asynchronously")
    def test_when_creating_the_same_user_then_it_returns_an_error(
        self, mock_email, unauthenticated_client
    ):
        assert User.objects.count() == 0

        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1

        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"non_field_errors: {ErrorCodes.EMAIL_EXISTS.value}"
        )
        assert User.objects.count() == 1

    def test_when_email_is_missing_then_an_error_is_returned(
        self, unauthenticated_client
    ):
        assert User.objects.count() == 0

        self.payload["email"] = ""
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "email: This field may not be blank."
        assert User.objects.count() == 0


class TestAccountActivateView:
    def setup_method(self):
        self.url = reverse("v1:user_activate-list")

    def test_can_activate_user_account(self, unauthenticated_client):
        assert User.objects.count() == 0
        user = baker.make(User, email="email@umoja.com")
        assert not user.is_active
        assert not user.verify_code
        assert not user.verify_code_expire
        updated_user = User.objects.generate_verify_code(user.email)
        assert updated_user.verify_code
        assert updated_user.verify_code_expire
        self.payload = {
            "email": updated_user.email,
            "verification_code": updated_user.verify_code,
        }
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_200_OK

    def test_user_does_not_exist(self, unauthenticated_client):
        self.payload = {"email": "doe@gmail.com", "verification_code": 125}
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "User does not exist."

    def test_invalid_verification_code(self, unauthenticated_client):
        assert User.objects.count() == 0
        user = baker.make(User, email="email@umoja.com")
        updated_user = User.objects.generate_verify_code(user.email)
        self.payload = {"email": updated_user.email, "verification_code": 895625}
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Verification code is invalid."

    def test_when_payload_is_invalid(self, unauthenticated_client):
        self.payload = {"email": "doe@gmail.com"}
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "verification_code: This field is required."


class TestResentAccountActivateView:
    def setup_method(self):
        self.url = reverse("v1:resend-verify-code-list")

    @patch("pycorpkit.accountx.usecases.register.send_email_asynchronously")
    def test_can_resend_signup_email(
        self, mock_email, user_profile, unauthenticated_client
    ):
        user = user_profile.user
        updated_user = User.objects.generate_verify_code(user.email)
        assert updated_user.verify_code
        assert updated_user.verify_code_expire
        self.payload = {
            "email": updated_user.email,
        }
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_200_OK
        mock_email.delay.assert_called_once()

    @patch("pycorpkit.accountx.usecases.register.send_email_asynchronously")
    def test_when_verify_code_is_missing(
        self, mock_email, user_profile, unauthenticated_client
    ):
        user = user_profile.user
        self.payload = {
            "email": user.email,
        }
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Verification code not found"
        mock_email.delay.assert_not_called()

    @patch("pycorpkit.accountx.usecases.register.send_email_asynchronously")
    def test_when_params_are_invalid(self, mock_email, unauthenticated_client):
        self.payload = {
            "idontExist": "mwas@gmail.com",
        }
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "email: This field is required."
        mock_email.delay.assert_not_called()
