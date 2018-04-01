from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueValidator


class SetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        style={'placeholder': 'User Name'},
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={'placeholder': 'Email', 'autofocus': True},
    )
    username = serializers.CharField(
        max_length=100,
        style={'placeholder': 'User Name'},
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


