from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_number', 'account_type', 'first_name', 'last_name', 'balance']


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_type', 'first_name', 'last_name', 'pin']
