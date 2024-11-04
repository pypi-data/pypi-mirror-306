from django.db import models

from pycorpkit.common.models.abstract import AbstractBase


class Invitation(AbstractBase):
    email = models.EmailField()
    accepted_invitation = models.BooleanField(default=False)
    accepted_time = models.DateTimeField(null=True, blank=True)
    invitation_sent = models.BooleanField(default=False)
