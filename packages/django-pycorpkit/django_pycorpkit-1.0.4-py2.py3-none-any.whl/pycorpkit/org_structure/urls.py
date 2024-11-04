from rest_framework.routers import DefaultRouter

from pycorpkit.org_structure.views.department_member import DepartmentMemberViewSet
from pycorpkit.org_structure.views.org_structure import BranchViewSet, DepartmentViewSet

department_router = DefaultRouter()
department_router.register(r"department", DepartmentViewSet, basename="department")
department_router.register(
    r"members", DepartmentMemberViewSet, basename="department_members"
)

branch_router = DefaultRouter()
branch_router.register(r"branch", BranchViewSet, basename="branch")
