from django.db import models

from pycorpkit.common.models.abstract import AbstractOrgDetails


class Branch(AbstractOrgDetails):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "branch"
