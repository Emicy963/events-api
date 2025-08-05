from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import User, UserProfile, OrganizerProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'user_type', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalide credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        return attrs

class UserProfileSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'bio', 'avatar', 'birth_day',
            'province', 'municipality', 'address', 'location',
            'sms_notifications', 'whatsapp_notifications', 'email_notifications'
        ]
        read_only_fields = ['user']

class OrganizerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerProfile
        fields = [
            'company_name', 'tax_id', 'company_logo', 'website', 'description',
            'is_verified', 'verification_documents',
            'comission_rate', 'total_events', 'total_sales'
        ]
        read_only_fields = ['user', 'is_verified', 'verification_documents', 'comission_rate', 'total_events', 'total_sales']
