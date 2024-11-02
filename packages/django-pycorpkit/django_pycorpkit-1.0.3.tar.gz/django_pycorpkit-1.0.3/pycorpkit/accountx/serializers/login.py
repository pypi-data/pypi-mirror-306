from rest_framework import serializers

from pycorpkit.common.serializers.profile import (
    ContactSerializer,
    PersonResponseSerializer,
    UserProfileSerializer,
)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, max_length=15)
    password = serializers.CharField(max_length=255)
    is_mobile_platform = serializers.BooleanField(default=False, required=False)

    def validate(self, data):
        """
        Check that at least one of email or phone is provided
        """
        if not data.get("email") and not data.get("phone"):
            raise serializers.ValidationError("Either email or phone must be provided")
        return data


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    surname = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    agreed_to_terms = serializers.BooleanField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    latitude = serializers.FloatField(required=False, allow_null=True)


class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    person = PersonResponseSerializer()
    profiles = UserProfileSerializer(many=True)
    contacts = ContactSerializer(many=True)
    permissions = serializers.DictField(source="permission_names")
    roles = serializers.DictField(source="role_names")
