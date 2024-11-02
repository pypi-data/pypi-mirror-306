import django_filters

from pycorpkit.common.filters.base import BaseFilter
from pycorpkit.org_structure.models import DepartmentMembers


class DepartmentMemberFilter(BaseFilter):

    first_name = django_filters.CharFilter(
        "user__person__first_name", lookup_expr="istartswith"
    )

    class Meta:
        model = DepartmentMembers
        fields = ["id"]
