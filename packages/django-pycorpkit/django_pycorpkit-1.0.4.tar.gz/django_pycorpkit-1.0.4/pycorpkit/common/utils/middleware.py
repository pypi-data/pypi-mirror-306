import logging

from django.apps import apps
from django.utils.deprecation import MiddlewareMixin

from pycorpkit.common.utils.conf import SETTINGS


LOGGER = logging.getLogger(__name__)


class OrganisationIDMiddleware(MiddlewareMixin):
    """
    Extract the current Organisation-ID from the request
    headers and attach it to the request object.
    """

    def process_request(self, request):
        organisation_id = request.headers.get("Organisation-ID")
        request.organisation_id = organisation_id
        request.organisation = None
        if organisation_id:
            try:
                Organisation = apps.get_model(
                    SETTINGS["CUSTOM_ORGANISATION_MODEL"], require_ready=False
                )
                request.organisation = Organisation.objects.get(id=organisation_id)
            except Organisation.DoesNotExist:
                LOGGER.info(
                    f"organisation id {organisation_id} not found", exc_info=True
                )
                request.organisation = None
