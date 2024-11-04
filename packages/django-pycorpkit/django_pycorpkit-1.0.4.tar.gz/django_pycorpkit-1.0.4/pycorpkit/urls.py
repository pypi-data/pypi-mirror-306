from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

from pycorpkit.accountx.urls import (
    invitations_router,
    password_router,
    permission_router,
    roles_router,
    user_router,
)
from pycorpkit.accountx.views.token import CustomTokenRefreshView
from pycorpkit.common.urls import organisation_router, profiles_router
from pycorpkit.org_structure.urls import branch_router, department_router

urlpatterns = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/", include(user_router.urls)),
    path("invitation/", include(invitations_router.urls)),
    path("profiles/", include(profiles_router.urls)),
    path("organisations/", include(organisation_router.urls)),
    path("branches/", include(branch_router.urls)),
    path("departments/", include(department_router.urls)),
    path("password/", include(password_router.urls)),
    path("roles/", include(roles_router.urls)),
    path("permissions/", include(permission_router.urls)),
]
