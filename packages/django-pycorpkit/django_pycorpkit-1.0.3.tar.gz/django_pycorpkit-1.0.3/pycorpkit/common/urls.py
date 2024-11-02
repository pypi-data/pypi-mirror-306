from rest_framework.routers import DefaultRouter

from pycorpkit.common.views.organisation import (
    OrganisationAttachmentViewSet,
    OrganisationCreateViewSet,
    OrganisationSimpleAttachmentViewSet,
    OrganisationViewSet,
)
from pycorpkit.common.views.profile import (
    UserProfileAttachmentViewSet,
    UserProfileViewSet,
)

profiles_router = DefaultRouter()
profiles_router.register(r"profile", UserProfileViewSet)
profiles_router.register(r"attachments", UserProfileAttachmentViewSet)

organisation_router = DefaultRouter()
organisation_router.register(r"organisation", OrganisationViewSet)
organisation_router.register(
    r"create", OrganisationCreateViewSet, basename="organisation_create"
)
organisation_router.register(r"attachments", OrganisationAttachmentViewSet)
organisation_router.register(
    r"attachment-simple",
    OrganisationSimpleAttachmentViewSet,
    basename="attchment_simple",
)
