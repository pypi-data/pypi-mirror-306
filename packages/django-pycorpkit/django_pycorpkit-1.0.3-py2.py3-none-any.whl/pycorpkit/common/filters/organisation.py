from pycorpkit.common.filters.base import BaseFilter
from pycorpkit.common.models.organisation import Organisation, OrganisationAttachment


class OrganisationFilter(BaseFilter):
    class Meta:
        model = Organisation
        fields = "__all__"


class OrganisationAttachmentFilter(BaseFilter):
    class Meta:
        model = OrganisationAttachment
        fields = (
            "organisation",
            "attachment",
            "created",
            "updated",
        )
