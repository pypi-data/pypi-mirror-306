import uuid

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from pycorpkit.common.models.attachment import Attachments


class OrganisationStatuses(models.TextChoices):
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"


class CommonAbstractOrganisation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    created_by = models.UUIDField(null=True, blank=True)
    updated_by = models.UUIDField(null=True, blank=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    email_address = models.EmailField(max_length=50, blank=True)
    phone_number = PhoneNumberField(blank=True)
    physical_address = models.TextField(blank=True)
    postal_address = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ("-updated", "-created")
        abstract = True


class Organisation(CommonAbstractOrganisation):
    """
    All resources are tied to an organisation.
    """

    name = models.CharField(max_length=255, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )
    registration_number = models.CharField(max_length=255, null=True, blank=True)
    kra_number = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OrganisationStatuses.choices,
        default=OrganisationStatuses.UNVERIFIED,
    )

    def __str__(self):
        return self.name

    @property
    def branches(self):
        return self.org_structure_branch_related.all()

    @property
    def members(self):
        return self.org_structure_departmentmembers_related.all()

    @property
    def departments(self):
        return self.org_structure_department_related.all()


class OrganisationAttachment(CommonAbstractOrganisation):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.PROTECT, related_name="organisation_attachments"
    )
    attachment = models.ForeignKey(
        Attachments,
        null=True,
        blank=True,
        related_name="attachments_organisation",
        on_delete=models.PROTECT,
    )
