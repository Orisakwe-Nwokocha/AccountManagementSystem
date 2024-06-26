from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account
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
    elif request.method == 'PATCH':
        serializer = AccountCreateSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # try:
    #     account = Account.objects.get(pk=account_number)
    #     serializer = AccountSerializer(account)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # except Account.DoesNotExist:
    #     return Response({"success": "false", "message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def deposit(request):
    account_number = request.data['account_number']
    print(account_number)
    amount = request.data['amount']
    account = get_object_or_404(Account, pk=account_number)
    print(account)
    if amount <= 0.0:
        raise ValueError("Amount must be greater than 0")
    account.balance += Decimal(amount)
    account.save()
    return Response(data={"success": True, "message": "Transaction successful"}, status=status.HTTP_200_OK)
