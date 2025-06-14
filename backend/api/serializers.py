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
            'rs_code',
            'supplier',
            'is_distributor',
            'is_supplier',
            'is_dealer',
        )


class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Dealer
        fields = (
            'id',
            'rs_code',
            'name',
            'inn',
            'phone',
            'user',
        )
