from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, AccountCreateSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def find_all(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = AccountCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_account(request, account_number):
    account = get_object_or_404(Account, pk=account_number)
    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = AccountCreateSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def deposit(request):
    account_number = request.data['account_number']
    amount = Decimal(request.data['amount'])
    account = get_object_or_404(Account, pk=account_number)
    if amount <= 0.0:
        return Response(data={"success": False, "message": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
    account.balance += amount
    account.save()
    Transaction.objects.create(
        account=account,
        amount=amount
    )
    return Response(data={"success": True, "message": "Transaction successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def withdraw(request):
    account_number = request.data['account_number']
    amount = Decimal(request.data['amount'])
    pin = request.data['pin']
    account = get_object_or_404(Account, pk=account_number)
    if account.pin != pin:
        return Response(data={"success": False, "message": "Invalid pin"}, status=status.HTTP_400_BAD_REQUEST)
    if amount <= 0:
        return Response(data={"success": False, "message": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
    if account.balance < amount:
        return Response(data={"success": False, "message": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
    account.balance -= amount
    account.save()
    Transaction.objects.create(
        account=account,
        amount=amount,
        transaction_type='DEB'
    )
    return Response(data={"success": True, "message": "Transaction successful"}, status=status.HTTP_200_OK)
