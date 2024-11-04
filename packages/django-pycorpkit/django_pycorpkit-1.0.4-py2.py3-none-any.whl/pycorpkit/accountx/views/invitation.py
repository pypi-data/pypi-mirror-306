import jwt
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from pycorpkit.accountx.filters.user import UserInviteFilter
from pycorpkit.accountx.models.invitation import Invitation
from pycorpkit.accountx.serializers.invitation import (
    AcceptInviteInput,
    InvitationSerializer,
    UserToInviteInput,
)
from pycorpkit.accountx.usecases.invitation import invite_new_user
from pycorpkit.common.usecases.organisation import (
    add_user_to_a_department,
    assign_a_role_to_a_user_profile,
)
from pycorpkit.common.utils.conf import SETTINGS
from pycorpkit.common.utils.helpers import PERMS, format_error_response
from pycorpkit.common.views.base import BaseViewSet


class InvitationViewSet(BaseViewSet):
    """
    Holds workflow for user invites.
    """

    permissions = {
        "GET": [PERMS.INVITE_VIEW],
        "POST": [PERMS.INVITE_CREATE],
        "PATCH": [PERMS.INVITE_EDIT],
        "DELETE": [PERMS.INVITE_DELETE],
    }
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    filterset_class = UserInviteFilter
    http_method_names = ["get", "post"]

    @action(methods=("post",), detail=False)
    def invite_user(self, request, *args, **kwargs):
        serializer = UserToInviteInput(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        user_serializer_data = serializer.validated_data
        new_user_input = {
            "email": user_serializer_data.get("email"),
            "role": user_serializer_data.get("role"),
            "department": user_serializer_data.get("department"),
            "profile": user_serializer_data.get("profile"),
            "organisation": request.organisation,
        }
        token = invite_new_user(**new_user_input)
        return Response(data={"token": token}, status=status.HTTP_200_OK)


class InvitationAcceptViewSet(BaseViewSet):
    """
    Holds workflow for accepting invites.
    """

    permissions = {
        "GET": [PERMS.INVITE_VIEW],
        "PATCH": [PERMS.INVITE_EDIT],
        "DELETE": [PERMS.INVITE_DELETE],
    }
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    filterset_class = UserInviteFilter
    http_method_names = ["post"]

    @transaction.atomic
    @action(methods=("post",), detail=False)
    def accept_invite(self, request, *args, **kwargs):
        serializer = AcceptInviteInput(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        serializer_data = serializer.validated_data
        payload = jwt.decode(
            serializer_data["token"], SETTINGS["SECRET_KEY"], algorithms=["HS256"]
        )
        email = payload.get("email")
        role = payload.get("role_id")
        profile = payload.get("profile_id")
        department = payload.get("department_id")
        serializer = UserToInviteInput(
            data={
                "email": email,
                "role": role,
                "department": department,
                "profile": profile,
            }
        )
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message="The invitation token is invalid",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        serializer_data = serializer.validated_data
        add_user_to_a_department(
            serializer_data["department"], serializer_data["profile"]
        )
        assign_a_role_to_a_user_profile(
            serializer_data["role"], serializer_data["profile"]
        )
        invite = Invitation.objects.get(email=email)
        invite.accepted_invitation = True
        invite.save()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
