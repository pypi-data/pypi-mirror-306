from django.db import models

from pycorpkit.common.models.abstract import AbstractBase, AbstractOrgDetails
from pycorpkit.common.models.profile import UserProfile
from pycorpkit.org_structure.models.branch import Branch


class Department(AbstractOrgDetails):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(
        Branch, on_delete=models.PROTECT, related_name="departments"
    )

    class Meta:
        db_table = "department"


class DepartmentMembers(AbstractBase):
    """
    A through model to manage the many-to-many relationship between UserProfile and Department.
    This allows profiles to be linked to multiple departments.
    It is also the basis of addressing the issue of an person having
    multiple profiles in different organizations.
    """

    user = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="user_department"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="department_users"
    )

    @property
    def user_details(self):
        return self.user.person

    class Meta:
        db_table = "department_members"
