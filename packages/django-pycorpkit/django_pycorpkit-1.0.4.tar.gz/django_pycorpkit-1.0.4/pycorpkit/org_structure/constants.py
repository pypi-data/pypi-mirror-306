from django.db import models


class OrganisationInviteStatuses(models.TextChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    EXPIRED = "EXPIRED"


class EmployeeTypeOption(models.TextChoices):
    PERMANENT = "PERMANENT"
    CONTRACT = "CONTRACT"
    LOCUM = "LOCUM"


class OrganisationEmployeeCategory(models.TextChoices):
    EMPLOYEE = "EMPLOYEE"
    CONSULTANT = "CONSULTANT"
