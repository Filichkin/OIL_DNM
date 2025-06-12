from rest_framework import serializers

from users.models import (
    Dealer,
    User
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role'
        )


class DealerReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = Dealer
        fields = (
            'id',
            'user',
            'rs_code',
            'name',
            'inn',
            'phone',
        )


class DealerAddSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = Dealer
        fields = (
            'id',
            'user',
            'rs_code',
            'name',
            'inn',
            'phone',
        )
