from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import User, UserProfile, OrganizerProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "phone",
            "user_type",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Password don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalide credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs["user"] = user
        return attrs


class UserProfileSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "bio",
            "avatar",
            "birth_day",
            "province",
            "municipality",
            "address",
            "location",
            "sms_notifications",
            "whatsapp_notifications",
            "email_notifications",
        ]
        read_only_fields = ["user"]


class OrganizerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerProfile
        fields = [
            "company_name",
            "tax_id",
            "company_logo",
            "website",
            "description",
            "is_verified",
            "verification_documents",
            "comission_rate",
            "total_events",
            "total_sales",
        ]
        read_only_fields = [
            "user",
            "is_verified",
            "verification_documents",
            "comission_rate",
            "total_events",
            "total_sales",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerialier()
    organizer_profile = OrganizerProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "user_type",
            "profile",
            "organizer_profile",
        ]
        read_only_fields = ["id", "email", "user_type"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        organizer_profile_data = validated_data.pop("organizer_profile", None)

        # Atualiza dados do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualiza perfil do usuário
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        # Atualiza perfil de organizador (se aplicável)
        if organizer_profile_data and hasattr(instance, "organizer_profile"):
            organizer_profile = instance.organizer_profile
            for attr, value in organizer_profile_data.items():
                setattr(organizer_profile, attr, value)
            organizer_profile.save()
        return instance
