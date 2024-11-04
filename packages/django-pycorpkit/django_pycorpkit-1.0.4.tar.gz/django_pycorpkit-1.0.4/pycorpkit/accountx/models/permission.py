from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from pycorpkit.common.models.abstract import AbstractBase


def validate_array_unique(value):
    if not len(value) == len(set(value)):
        raise ValidationError("Ensure the permission's children provided are unique.")


class Permissions(AbstractBase):
    """
    This model maintains a flat structure for permissions at the data layer.
    """

    name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    is_deprecated = models.BooleanField(default=False)
    is_system_level = models.BooleanField(default=False)
    children = ArrayField(
        models.CharField(max_length=200),
        null=True,
        blank=True,
        validators=[validate_array_unique],
    )
    organisation = None

    def validate_parent_not_in_children(self):
        if self.children:
            if self.name in self.children:
                raise ValidationError(
                    {
                        "children": (
                            "Ensure that the parent permission is not "
                            "included in its children."
                        )
                    }
                )

    def validate_child_perm_exists(self):
        if self.children:
            existing = self.__class__.objects.filter(name__in=self.children).count()
            if len(self.children) != existing:
                msg = "Please ensure the children to {} are already created"
                raise ValidationError({"children": msg.format(self.name)})

    def clean(self, *args, **kwargs):
        self.validate_parent_not_in_children()
        self.validate_child_perm_exists()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
