from django.contrib.auth import authenticate
from rest_framework import serializers

from clients.models import CustomUser
from clients.utils.base64 import Base64ImageField


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('avatar', 'gender', 'first_name', 'last_name', 'email',
                  'password')

    def validate_email(self, data):
        if CustomUser.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                'Такой email уже существует.')
        return data


class CustomObtainAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'gender', 'first_name', 'last_name', 'email')
