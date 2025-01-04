from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from users.models import User
from users.serializers import UserResponseSerializer


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        refresh = RefreshToken.for_user(user)
        user_serializer = UserResponseSerializer(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data
        }


class TokenOutputSerializer(serializers.Serializer):  # noqa
    refresh = serializers.CharField(label=_("Refresh token"))
    access = serializers.CharField(label=_("Access token"))
    user = UserResponseSerializer(label=_("User information"))


class UserLogoutSerializer(serializers.Serializer):  # noqa
    user = serializers.CharField()
    auth_user = serializers.CharField()

    def validate(self, data):
        if data['user'] != data['auth_user']:
            raise serializers.ValidationError('Invalid operation')
        user = User.objects.get(username=data['user'])
        self.context['user'] = user
        return data

    def save(self):
        RefreshToken.for_user(self.context['user'])


class LogoutSerializer(serializers.Serializer):  # noqa
    refresh_token = serializers.CharField()


class ResetPasswordRequestSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField(required=True)

class ResetPasswordCodeValidateRequestSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

class ValidateCodeRequestSerializer(serializers.Serializer):
    token = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class GenerateCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)