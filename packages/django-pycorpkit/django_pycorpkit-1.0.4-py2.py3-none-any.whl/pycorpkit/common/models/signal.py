from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from pycorpkit.common.models.organisation import Organisation
from pycorpkit.common.usecases.organisation import initialize_organisation
from pycorpkit.common.utils.helpers import get_default_roles


@receiver(post_save, dispatch_uid="setup_organisation", sender=Organisation)
def setup_organisation(instance, created, **kwargs):
    if not created:
        return

    roles_and_perms = get_default_roles().items()
    initialize_organisation(instance, roles_and_perms)
