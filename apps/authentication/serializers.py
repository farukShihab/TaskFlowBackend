from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Used whenever user information is returned to the frontend.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "created_at",
            "date_joined",
        )
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Used to register a new user.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )

    def validate_email(self, value):
        email = value.lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return email

    def validate_username(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )

        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    """
    Used only to validate login credentials.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")

        user = authenticate(
            username=email,   # USERNAME_FIELD = "email"
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account has been disabled."
            )

        attrs["user"] = user
        return attrs