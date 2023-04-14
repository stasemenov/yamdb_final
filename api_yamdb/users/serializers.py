from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'bio',
            'email', 'role',
        )


class UserSerializer(BaseUserSerializer):
    pass


class MeSerializer(BaseUserSerializer):
    role = serializers.CharField(read_only=True)


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('email', 'username'),
                message='Поля email и username должны быть уникальными'
            )
        ]

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено')
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     validators=[UnicodeUsernameValidator],
                                     required=True)
    confirmation_code = serializers.CharField(required=True)
