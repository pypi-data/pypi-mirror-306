from pycorpkit.common.utils.helpers import PERMS
from pycorpkit.common.views.base import BaseViewSet
from pycorpkit.org_structure.filters.department_member import DepartmentMemberFilter
from pycorpkit.org_structure.models import DepartmentMembers
from pycorpkit.org_structure.serializers.orgs_serializers import (
    DepartmentMemberReadSerializer,
)


class DepartmentMemberViewSet(BaseViewSet):
    permissions = {
        "GET": [PERMS.DEPARTMENT_VIEW],
        "PATCH": [PERMS.DEPARTMENT_EDIT],
        "POST": [PERMS.DEPARTMENT_CREATE],
        "DELETE": [PERMS.DEPARTMENT_DELETE],
    }
    queryset = DepartmentMembers.objects.filter(active=True).all()
    serializer_class = DepartmentMemberReadSerializer
    filterset_class = DepartmentMemberFilter
    http_method_names = ["get", "post", "patch", "options"]
