from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from pycorpkit.common.filters.organisation import (
    OrganisationAttachmentFilter,
    OrganisationFilter,
)
from pycorpkit.common.models.attachment import Attachments
from pycorpkit.common.models.organisation import Organisation, OrganisationAttachment
from pycorpkit.common.serializers.organisation import (
    OrganisationAttachmentSerializer,
    OrganisationAttachmentsUploadSerializer,
    OrganisationSerializer,
)
from pycorpkit.common.utils.helpers import PERMS
from pycorpkit.common.views.base import BaseViewSet


class OrganisationViewSet(BaseViewSet):
    """
    This supports get and update operations only when authenticated.
    """

    permissions = {
        "GET": [PERMS.ORGANISATION_VIEW],
        "PATCH": [PERMS.ORGANISATION_EDIT],
        "DELETE": [PERMS.ORGANISATION_DELETE],
    }
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filterset_class = OrganisationFilter
    http_method_names = ["get", "patch", "options"]


class OrganisationCreateViewSet(OrganisationViewSet):
    """
    This allows users create organisations when not authenticated.
    """

    permissions = {
        "GET": [PERMS.ORGANISATION_VIEW],
        "PATCH": [PERMS.ORGANISATION_EDIT],
        "DELETE": [PERMS.ORGANISATION_DELETE],
    }
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filterset_class = OrganisationFilter
    permission_classes = [AllowAny]
    http_method_names = ["post", "options"]


class OrganisationAttachmentViewSet(BaseViewSet):
    """
    This allows users to upload attachments when not authenticated.
    """

    queryset = OrganisationAttachment.objects.all()
    serializer_class = OrganisationAttachmentSerializer
    filterset_class = OrganisationAttachmentFilter
    permission_classes = [AllowAny]
    http_method_names = ["post", "options"]

    @transaction.atomic
    @action(methods=("post",), detail=False)
    def upload_attachment(self, request, *args, **kwargs):
        serializer = OrganisationAttachmentsUploadSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        default_data = {"created_by": request.user.id, "updated_by": request.user.id}
        validated_data = serializer.validated_data

        attachment_data = {
            "content_type": validated_data["content_type"],
            "uploaded_file": validated_data["attachment"],
            "title": validated_data["attachment"].name,
            "size": validated_data["attachment"].size,
            "description": validated_data.get("description"),
        }
        attachment_data.update(default_data)
        attachment = Attachments.objects.create(**attachment_data)

        organisation_attachment_data = {
            "organisation": validated_data.get("organisation"),
            "attachment": attachment,
        }
        organisation_attachment_data.update(default_data)
        organisation_attachment = OrganisationAttachment.objects.create(
            **organisation_attachment_data
        )
        response_serializer = self.get_serializer(organisation_attachment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrganisationSimpleAttachmentViewSet(BaseViewSet):
    """
    This supports read and update operations only when authenticated.
    """

    permissions = {
        "GET": [PERMS.ORGANISATION_VIEW],
        "PATCH": [PERMS.ORGANISATION_EDIT],
        "DELETE": [PERMS.ORGANISATION_DELETE],
    }
    queryset = OrganisationAttachment.objects.all()
    serializer_class = OrganisationAttachmentSerializer
    filterset_class = OrganisationAttachmentFilter
    http_method_names = ["get", "patch", "options"]
