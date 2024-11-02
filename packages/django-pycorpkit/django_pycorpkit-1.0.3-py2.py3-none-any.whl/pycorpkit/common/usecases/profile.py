from django.db.transaction import atomic

from pycorpkit.common.models.attachment import Attachments
from pycorpkit.common.models.profile import UserProfileAttachment


@atomic
def create_profile_attachment(validated_data, user):
    default_data = {"created_by": user.id, "updated_by": user.id}

    attachment = Attachments.objects.create(
        content_type=validated_data["content_type"],
        uploaded_file=validated_data["attachment"],
        title=validated_data["attachment"].name,
        size=validated_data["attachment"].size,
        description=validated_data.get("description"),
        **default_data
    )

    profile_attachment_data = {
        "profile": validated_data.get("profile"),
        "attachment": attachment,
    }
    profile_attachment_data.update(default_data)
    return UserProfileAttachment.objects.create(**profile_attachment_data)
