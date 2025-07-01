from rest_framework import serializers

from users.models import (
    Dealer,
    Supplier,
    User
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'first_name',
            'last_name',
            'rs_code',
            'supplier',
            'is_distributor',
            'is_supplier',
            'is_dealer',
            'is_dealer_admin'
        )


class UserDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'first_name',
            'last_name',
            'is_dealer_admin'
        )


class DealerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dealer
        fields = (
            'id',
            'rs_code',
            'name',
            'inn',
            'address',
            'legal_address',
        )


class DealerReadSerializer(serializers.ModelSerializer):
    users = UserDealerSerializer(
        read_only=True,
        many=True,
        source='dealer_users'
        )

    class Meta:
        model = Dealer
        fields = (
            'id',
            'rs_code',
            'name',
            'inn',
            'address',
            'legal_address',
            'users',
        )


class SupplierCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'legal_name',
            'inn',
            'phone',
            'contact_name',
            'contact_job_title',
            'address',
            'legal_address'
            )


class SupplierReadSerializer(serializers.ModelSerializer):
    users = UserSerializer(
        read_only=True,
        many=True,
        source='supplier_users'
        )

    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'legal_name',
            'inn',
            'phone',
            'contact_name',
            'contact_job_title',
            'address',
            'legal_address',
            'users'
            )
