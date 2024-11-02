from django.contrib import admin
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

v1_urls = [
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/", include(user_router.urls)),
    path("invitation/", include(invitations_router.urls)),
    path("profiles/", include(profiles_router.urls)),
    path("organisations/", include(organisation_router.urls)),
    path("password/", include(password_router.urls)),
    path("roles/", include(roles_router.urls)),
    path("permissions/", include(permission_router.urls)),
]


urlpatterns = [
    path("api/v1/", include((v1_urls, "v1"), namespace="v1")),
    path("admin/", admin.site.urls),
] 
