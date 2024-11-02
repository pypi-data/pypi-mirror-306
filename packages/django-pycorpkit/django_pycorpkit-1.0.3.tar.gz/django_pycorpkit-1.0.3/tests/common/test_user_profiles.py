import os

import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from pycorpkit.common.models.attachment import Attachments
from pycorpkit.common.models.profile import UserProfileAttachment

pytestmark = pytest.mark.django_db


class TestProfileViews:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, client_without_org):
        self.client = client_without_org
        self.url = reverse("v1:userprofile-list")

    def test_can_list_profiles(self, profile_in_org):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("page_size") == 40
        assert response.data.get("current_page") == 1
        assert response.data.get("total_pages") == 1

    def test_when_all_details_are_provided_then_userprofile_is_updated(
        self, user_profile
    ):
        assert user_profile.person.first_name == "John"
        assert user_profile.person.last_name == "Doe"
        assert user_profile.person.phone_number == "0700100200"
        assert user_profile.person.email == "mail@mail.com"
        assert not user_profile.person.id_number
        assert not user_profile.person.gender
        assert not user_profile.person.date_of_birth
        url = reverse("v1:userprofile-update-user-profile")
        data = {
            "user": user_profile.user.id,
            "first_name": "Rapcha",
            "last_name": "Scientist",
            "id_number": "100001",
            "date_of_birth": "1996-01-01",
            "phone_number": "0799100200",
            "email": "rapcha@gmail.com",
            "gender": "male",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("person")["first_name"] == data["first_name"]
        assert response.data.get("person")["last_name"] == data["last_name"]
        assert response.data.get("person")["date_of_birth"] == data["date_of_birth"]
        assert response.data.get("person")["email"] == data["email"]
        assert response.data.get("person")["phone_number"] == data["phone_number"]
        assert response.data.get("person")["id_number"] == data["id_number"]
        assert response.data.get("person")["gender"] == data["gender"]

    def test_when_partial_details_are_provided_then_userprofile_is_updated(
        self, user_profile
    ):
        assert user_profile.person.first_name == "John"
        assert user_profile.person.last_name == "Doe"
        assert user_profile.person.phone_number == "0700100200"
        assert user_profile.person.email == "mail@mail.com"
        assert not user_profile.person.id_number
        assert not user_profile.person.gender
        assert not user_profile.person.date_of_birth
        url = reverse("v1:userprofile-update-user-profile")
        data = {
            "user": user_profile.user.id,
            "id_number": "100001",
            "date_of_birth": "1996-01-01",
            "gender": "male",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data.get("person")["first_name"] == user_profile.person.first_name
        )
        assert response.data.get("person")["last_name"] == user_profile.person.last_name
        assert (
            response.data.get("person")["phone_number"] == user_profile.person.phone_number
        )
        assert response.data.get("person")["date_of_birth"] == data["date_of_birth"]
        assert response.data.get("person")["id_number"] == data["id_number"]
        assert response.data.get("person")["gender"] == data["gender"]

    def test_when_user_is_missing_then_profile_is_not_updated(self):
        url = reverse("v1:userprofile-update-user-profile")
        data = {
            "id_number": "100001",
            "date_of_birth": "1996-01-01",
            "gender": "male",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "user: This field is required."


class TestProfileFilters:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, user_profile, client_without_org):
        self.client = client_without_org
        self.profile = user_profile
        self.url = reverse("v1:userprofile-list")

    def test_can_filter_by_user_id(self):
        filters = {"user_id": self.profile.user.id}
        response = self.client.get(self.url, filters)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("page_size") == 40
        assert response.data.get("current_page") == 1
        assert response.data.get("total_pages") == 1


class TestProfileAttachments:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, user_profile, client_without_org):
        self.profile = user_profile
        self.url = "v1:userprofileattachment"
        self.client = client_without_org

    def test_can_upload_attachment(self):
        assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets")
        )
        data = File(open(assets_dir + "/dummy.pdf", "rb"))
        upload_file = SimpleUploadedFile(
            "dummy.pdf", data.read(), content_type="application/pdf"
        )

        url = reverse(self.url + "-upload-attachment")
        payload = {"attachment": upload_file, "profile": self.profile.pk}
        resp = self.client.post(
            url,
            payload,
            content_disposition="attachment; filename=dummy.pdf",
            format="multipart",
        )
        assert resp.status_code == 201, resp.content
        assert Attachments.objects.count() == 1
        attachment = Attachments.objects.first()
        assert attachment.content_type == "application/pdf"
        assert UserProfileAttachment.objects.count() == 1
        profile_att = UserProfileAttachment.objects.first()
        assert profile_att.profile == self.profile
        assert profile_att.attachment == attachment
