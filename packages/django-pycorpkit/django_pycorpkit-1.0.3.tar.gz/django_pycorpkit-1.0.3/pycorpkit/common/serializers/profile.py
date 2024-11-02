from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from pycorpkit.accountx.models.user import User
from pycorpkit.common.models.person import Person
from pycorpkit.common.models.profile import UserProfile, UserProfileAttachment
from pycorpkit.common.serializers.common import (
    AttachmentsUploadSerializer,
    BaseModelSerializer,
)


class UserProfileSerializer(BaseModelSerializer):

    class Meta:
        model = UserProfile
        exclude = [
            "created",
            "updated",
            "deleted_at",
            "active",
            "user",
            "person",
            "created_by",
            "updated_by",
            "search_vector",
        ]


class PersonSerializer(BaseModelSerializer):

    class Meta:
        model = Person
        exclude = [
            "created",
            "updated",
            "deleted_at",
            "created_by",
            "updated_by",
        ]


class PersonResponseSerializer(BaseModelSerializer):
    phone_number = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    is_bio_data_captured = serializers.ReadOnlyField()

    class Meta:
        model = Person
        exclude = [
            "created",
            "updated",
            "deleted_at",
            "created_by",
            "updated_by",
        ]


class PersonBioDataSerializer(serializers.Serializer):
    id_number = serializers.IntegerField(required=True)
    date_of_birth = serializers.DateField(required=True)


class UserProfileAttachmentSerializer(BaseModelSerializer):
    title = serializers.ReadOnlyField(source="attachment.title")
    description = serializers.ReadOnlyField(source="attachment.description")
    url = serializers.FileField(source="attachment.uploaded_file", read_only=True)

    class Meta:
        model = UserProfileAttachment
        exclude = [
            "created",
            "updated",
            "deleted_at",
            "active",
            "created_by",
            "updated_by",
        ]


class ProfileAttachmentsUploadSerializer(AttachmentsUploadSerializer):
    profile = PrimaryKeyRelatedField(queryset=UserProfile.objects.all())


class ContactSerializer(serializers.Serializer):
    contact_type = serializers.ChoiceField(choices=["EMAIL", "PHONE"])
    contact_value = serializers.CharField()
    is_primary = serializers.BooleanField()


class UpdateProfileInputSerializer(serializers.Serializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    id_number = serializers.IntegerField(required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
