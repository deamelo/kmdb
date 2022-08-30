from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Account

class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=127)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField()
    bio = serializers.CharField(default=None)
    is_critic = serializers.BooleanField(default=False)
    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.ReadOnlyField()


    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Account.objects.all(),
                fields=['username', 'email']
            )
        ]

    def create(self, validated_data: dict) -> Account:
        account = Account.objects.create_user(**validated_data)

        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
