from rest_framework import serializers

from account.models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'transaction_type', 'transaction_time',
                  'transaction_status', 'description']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Account
        fields = ['account_number', 'account_type', 'first_name', 'last_name', 'balance', 'transactions']
        # transactions = serializers.StringRelatedField


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_type', 'first_name', 'last_name', 'pin']
