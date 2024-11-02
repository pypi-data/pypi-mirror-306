import os

import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from pycorpkit.common.models.attachment import Attachments
from pycorpkit.common.models.organisation import OrganisationAttachment, OrganisationStatuses
from pycorpkit.common.utils.error_codes import ErrorCodes
from tests.helpers import create_test_user


class TestOrganisationViews:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, client):
        self.client = client
        self.url = reverse("v1:organisation-list")

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "organisation_list"}], indirect=True
    )
    def test_can_list_organisations_only_when_authenticated(
        self, assign_permission, organisation
    ):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("page_size") == 40
        assert response.data.get("current_page") == 1
        assert response.data.get("total_pages") == 1
        assert len(response.data.get("results")) == 2
        assert response.data.get("results")[1].get("name") == organisation.name

    def test_when_not_authenticated_then_cannot_list_organisations(self, organisation):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "You do not have permission to perform this action."
        )

    def test_when_not_authenticated_then_an_organisation_can_be_created(
        self, client_without_org
    ):
        data = {
            "name": "BusPas Electric",
            "email_address": "kangethe@gmail.com",
            "phone_number": "0715489523",
        }
        url = reverse("v1:organisation_create-list")
        response = client_without_org.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("name") == data["name"]
        assert response.data.get("status") == OrganisationStatuses.UNVERIFIED
        assert not response.data.get("registration_number")

    def test_when_organisation_name_exists_then_it_cannot_be_created(
        self, client_without_org, organisation
    ):
        data = {
            "name": organisation.name,
            "email_address": "kangethe@gmail.com",
            "phone_number": "0715489523",
        }
        url = reverse("v1:organisation_create-list")
        response = client_without_org.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"name: {ErrorCodes.ORGANISATION_NAME_EXIST.value}"
        )

    def test_when_a_user_with_similar_email_exists_then_it_cannot_be_created(
        self, client_without_org
    ):
        common_email = "uhasibu@gmail.com"
        create_test_user(username=common_email, email=common_email)
        data = {
            "name": "BBR Healthcare",
            "email_address": common_email,
            "phone_number": "0715489523",
        }
        url = reverse("v1:organisation_create-list")
        response = client_without_org.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"email_address: {ErrorCodes.EMAIL_EXISTS.value}"
        )

    def test_when_organisation_email_exists_then_it_cannot_be_created(
        self, client_without_org, organisation
    ):
        data = {
            "name": "BBR Healthcare",
            "email_address": organisation.email_address,
            "phone_number": "0715489523",
        }
        url = reverse("v1:organisation_create-list")
        response = client_without_org.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"email_address: {ErrorCodes.ORGANISATION_EMAIL_EXISTS.value}" # noqa
        )

    def test_when_organisation_email_is_invalid_then_it_cannot_be_created(
        self, client_without_org
    ):
        data = {
            "name": "BBR Healthcare",
            "email_address": "mwas@gmail",
            "phone_number": "0715489523",
        }
        url = reverse("v1:organisation_create-list")
        response = client_without_org.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "email_address: Enter a valid email address."

    def test_when_organisation_phone_exists_then_it_cannot_be_created(
        self, unauthenticated_client, organisation
    ):
        data = {
            "name": "BBR Healthcare",
            "email_address": "bbr@gmail.com",
            "phone_number": str(organisation.phone_number.national_number),
        }
        url = reverse("v1:organisation_create-list")
        response = unauthenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"phone_number: {ErrorCodes.ORGANISATION_PHONE_EXISTS.value}" # noqa
        )

    def test_when_organisation_phone_is_invalid_then_it_cannot_be_created(
        self, unauthenticated_client
    ):
        data = {
            "name": "BBR Healthcare",
            "email_address": "bbr@gmail.com",
            "phone_number": "07124",
        }
        url = reverse("v1:organisation_create-list")
        response = unauthenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"phone_number: {ErrorCodes.INVALID_PHONE_NUMBER.value}"
        )


class TestOrgansationDetailViews:

    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, organisation, client):
        self.organisation = organisation
        self.client = client
        self.url = reverse("v1:organisation-detail", args=(self.organisation.id,))

    def test_when_not_authenticated_then_an_organisation_cannot_be_fethed(
        self,
    ):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "You do not have permission to perform this action."
        )

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "organisation_edit"}], indirect=True
    )
    def test_can_update_an_organisation(self, assign_permission, organisation):
        assert not organisation.registration_number
        data = {"registration_number": "145896"}
        response = self.client.patch(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("registration_number") == data["registration_number"]


class TestOrganisationFilters:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, organisation, client):
        self.client = client
        self.organisation = organisation
        self.url = reverse("v1:organisation-list")

    @pytest.mark.parametrize(
        "assign_permission", [{"perm_name": "organisation_list"}], indirect=True
    )
    def test_cannot_filter_non_existent_organisations(self, assign_permission):
        filters = {"name": "IdontExist"}
        response = self.client.get(self.url, filters)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("results") == []


class TestOrganisationAttachments:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, organisation, client_without_org):
        self.organisation = organisation
        self.url = "v1:organisationattachment"
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
        payload = {"attachment": upload_file, "organisation": self.organisation.pk}
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
        assert OrganisationAttachment.objects.count() == 1
        organisation_att = OrganisationAttachment.objects.first()
        assert organisation_att.organisation == self.organisation
        assert organisation_att.attachment == attachment
