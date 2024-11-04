from rest_framework import serializers

from pycorpkit.common.serializers.common import BaseModelSerializer
from pycorpkit.common.serializers.profile import PersonResponseSerializer
from pycorpkit.org_structure.models.branch import Branch
from pycorpkit.org_structure.models.department import Department, DepartmentMembers


class DepartmentResponseSerializer(BaseModelSerializer):
    organisation_name = serializers.ReadOnlyField(source="organisation.name")
    branch_name = serializers.ReadOnlyField(source="branch.name")
    email_address = serializers.ReadOnlyField()
    phone_number = serializers.ReadOnlyField()

    class Meta:
        model = Department
        exclude = [
            "deleted_at",
            "created",
            "updated",
            "updated_by",
            "created_by",
            "physical_address",
            "postal_address",
            "active",
        ]


class DepartmentMemberReadSerializer(BaseModelSerializer):
    user_details = PersonResponseSerializer(read_only=True)

    class Meta:
        model = DepartmentMembers
        exclude = [
            "active",
            "created",
            "updated",
            "deleted_at",
            "created_by",
            "updated_by",
        ]


class BranchResponseSerializer(BaseModelSerializer):

    class Meta:
        model = Branch
        exclude = ["deleted_at"]
