from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.organisation import Organisation, OrganisationAttachment
from pycorpkit.common.serializers.common import (
    AttachmentsUploadSerializer,
    BaseModelSerializer,
)
from pycorpkit.common.utils.error_codes import ErrorCodes
from pycorpkit.common.utils.helpers import InvalidPhoneNumber, validate_a_phone_number
from pycorpkit.org_structure.serializers.orgs_serializers import (
    BranchResponseSerializer,
    DepartmentMemberReadSerializer,
    DepartmentResponseSerializer,
)


class OrganisationSerializer(BaseModelSerializer):
    departments = DepartmentResponseSerializer(many=True, read_only=True)
    branches = BranchResponseSerializer(many=True, read_only=True)
    members = DepartmentMemberReadSerializer(many=True, read_only=True)
    email_address = serializers.EmailField()
    name = serializers.CharField(max_length=50)
    phone_number = serializers.CharField()

    class Meta:
        model = Organisation
        exclude = [
            "deleted",
            "parent",
            "updated",
            "active",
            "created_by",
            "updated_by",
        ]

    def validate_name(self, value):
        if Organisation.objects.filter(name=value).exists():
            raise serializers.ValidationError(ErrorCodes.ORGANISATION_NAME_EXIST.value)
        return value

    def validate_email_address(self, value):
        validate_email(value)

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(ErrorCodes.EMAIL_EXISTS.value)

        if Organisation.objects.filter(email_address=value).exists():
            raise serializers.ValidationError(
                ErrorCodes.ORGANISATION_EMAIL_EXISTS.value
            )
        return value

    def validate_phone_number(self, value):
        try:
            parsed_number = validate_a_phone_number(value, "KE")
        except InvalidPhoneNumber:
            raise serializers.ValidationError(ErrorCodes.INVALID_PHONE_NUMBER.value)

        if Organisation.objects.filter(phone_number=parsed_number).exists():
            raise serializers.ValidationError(
                ErrorCodes.ORGANISATION_PHONE_EXISTS.value
            )
        return parsed_number


class OrganisationAttachmentSerializer(BaseModelSerializer):
    title = serializers.ReadOnlyField(source="attachment.title")
    description = serializers.ReadOnlyField(source="attachment.description")
    url = serializers.FileField(source="attachment.uploaded_file", read_only=True)

    class Meta:
        model = OrganisationAttachment
        exclude = [
            "updated",
            "deleted",
            "active",
            "updated_by",
        ]


class OrganisationAttachmentsUploadSerializer(AttachmentsUploadSerializer):
    organisation = PrimaryKeyRelatedField(queryset=Organisation.objects.all())
