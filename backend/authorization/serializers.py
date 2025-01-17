from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from authorization.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError('A user with this email not found.')
        if not user.check_password(password):
            raise serializers.ValidationError('The password is incorrect.')
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'username': user.username,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get('refresh')
        access = attrs.get('access')
        try:
            RefreshToken(refresh)
        except Exception:
            raise serializers.ValidationError('Token is invalid or has expired.')
        return {
            'refresh': refresh,
            'access': access
        }
