from pycorpkit.accountx.filters.user import UserFilter
from pycorpkit.accountx.models.user import User
from pycorpkit.accountx.serializers.login import UserSerializer
from pycorpkit.common.utils.helpers import PERMS
from pycorpkit.common.views.base import BaseViewSet


class UserViewSet(BaseViewSet):
    """
    Adds ability to fetch a user details.
    """

    permissions = {
        "POST": [PERMS.USER_CREATE],
        "PATCH": [PERMS.USER_EDIT],
        "DELETE": [PERMS.USER_DELETE],
    }
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    http_method_names = ["get"]
