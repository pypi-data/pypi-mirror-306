from pycorpkit.common.utils.helpers import PERMS
from pycorpkit.common.views.base import BaseViewSet
from pycorpkit.org_structure.filters.org_structure import BranchFilter, DepartmentFilter
from pycorpkit.org_structure.models.branch import Branch
from pycorpkit.org_structure.models.department import Department
from pycorpkit.org_structure.serializers.orgs_serializers import (
    BranchResponseSerializer,
    DepartmentResponseSerializer,
)


class BranchViewSet(BaseViewSet):
    permissions = {
        "GET": [PERMS.BRANCH_VIEW],
        "PATCH": [PERMS.BRANCH_EDIT],
        "POST": [PERMS.BRANCH_CREATE],
        "DELETE": [PERMS.BRANCH_DELETE],
    }
    queryset = Branch.objects.filter(active=True).all()
    serializer_class = BranchResponseSerializer
    filterset_class = BranchFilter
    http_method_names = ["get", "post", "patch", "options"]


class DepartmentViewSet(BaseViewSet):
    permissions = {
        "GET": [PERMS.DEPARTMENT_VIEW],
        "PATCH": [PERMS.DEPARTMENT_EDIT],
        "POST": [PERMS.DEPARTMENT_CREATE],
        "DELETE": [PERMS.DEPARTMENT_DELETE],
    }
    queryset = Department.objects.filter(active=True).all()
    serializer_class = DepartmentResponseSerializer
    filterset_class = DepartmentFilter
    http_method_names = ["get", "post", "patch", "options"]
