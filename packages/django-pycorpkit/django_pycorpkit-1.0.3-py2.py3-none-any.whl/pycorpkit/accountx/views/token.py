from rest_framework_simplejwt.views import TokenRefreshView

from pycorpkit.accountx.serializers.token import CustomTokenRefreshSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
