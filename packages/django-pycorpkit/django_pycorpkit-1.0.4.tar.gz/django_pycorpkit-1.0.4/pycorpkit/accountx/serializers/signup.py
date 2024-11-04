from rest_framework import serializers

from pycorpkit.accountx.models.user import User
from pycorpkit.common.utils.error_codes import ErrorCodes


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, max_length=15)
    password = serializers.CharField()

    def validate(self, data):
        email = data["email"]
        if not email:
            raise serializers.ValidationError(ErrorCodes.MISSING_EMAIL.value)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(ErrorCodes.EMAIL_EXISTS.value)

        return data


class RegistrationResponseSerializer(serializers.Serializer):
    user_id = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)


class ActivateUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    verification_code = serializers.CharField(max_length=255)


class ResendActivateUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
