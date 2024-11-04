from pycorpkit.common.filters.base import BaseFilter
from pycorpkit.org_structure.models.branch import Branch
from pycorpkit.org_structure.models.department import Department


class BranchFilter(BaseFilter):

    class Meta:
        model = Branch
        fields = "__all__"


class DepartmentFilter(BaseFilter):

    class Meta:
        model = Department
        fields = "__all__"
