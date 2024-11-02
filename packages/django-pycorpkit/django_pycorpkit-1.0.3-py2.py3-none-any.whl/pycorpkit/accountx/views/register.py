from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from pycorpkit.accountx.models.user import User
from pycorpkit.accountx.serializers.signup import (
    ActivateUserSerializer,
    RegistrationResponseSerializer,
    RegistrationSerializer,
    ResendActivateUserSerializer,
)
from pycorpkit.accountx.usecases.register import (
    register_user,
    send_user_activation_email,
)
from pycorpkit.common.utils.helpers import format_error_response


class RegisterUserViewSet(viewsets.ViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        result, status_code = register_user(serializer.validated_data)
        user_id = result.get("user_id")
        if not user_id:
            return Response(result, status=status_code)

        serialized_data = RegistrationResponseSerializer(result).data
        return Response(serialized_data, status=status_code)


class ActivateUserViewSet(viewsets.ViewSet):
    """
    This verifies the email that was used during signup.
    """

    serializer_class = ActivateUserSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        email = serializer.validated_data.get("email")
        verification_code = serializer.validated_data.get("verification_code")
        User.objects.make_user_active(email, verification_code)
        return Response({}, status=status.HTTP_200_OK)


class ResendActivationEmailViewSet(viewsets.ViewSet):
    """
    This resends the activation email on signup.
    This is called when the user did not receive the email.
    """

    serializer_class = ResendActivateUserSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)
        if not user.verify_code:
            data, status_code = format_error_response(
                message="Verification code not found",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)
        send_user_activation_email(user)
        return Response({}, status=status.HTTP_200_OK)
