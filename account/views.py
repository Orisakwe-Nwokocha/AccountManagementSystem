import datetime
from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Account, Transaction
from .serializers import AccountCreateSerializer, DepositSerializer, WithdrawSerializer


# Create your views here.


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer


# class FindAll(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer

# def get_queryset(self):
#     return Account.objects.all()
#
# def get_serializer_class(self):
#     return AccountCreateSerializer

# @staticmethod
# def get(request):
#     accounts = Account.objects.all()
#     serializer = AccountSerializer(accounts, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# @staticmethod
# def post(request):
#     serializer = AccountCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class FindAccount(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer

# @staticmethod
# def get(request, account_number):
#     account = get_object_or_404(Account, pk=account_number)
#     serializer = AccountSerializer(account)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# @staticmethod
# def put(request, account_number):
#     account = get_object_or_404(Account, pk=account_number)
#     serializer = AccountSerializer(account, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# @staticmethod
# def delete(request, account_number):
#     account = get_object_or_404(Account, pk=account_number)
#     account.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class Deposit(APIView):
    @staticmethod
    def post(request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        amount = Decimal(serializer.data['amount'])
        account = get_object_or_404(Account, pk=account_number)
        response = build_response(True, account_number, amount,
                                  'CREDIT', 'Transaction successful')
        if amount <= 0.0:
            response['success'] = False
            response['message'] = "Amount must be greater than 0"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        balance = account.balance
        balance += amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        Transaction.objects.create(
            account=account,
            amount=amount
        )

        return Response(data=response, status=status.HTTP_200_OK)


class Withdraw(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.data['account_number']
        amount = Decimal(serializer.data['amount'])
        pin = serializer.data['pin']
        account = get_object_or_404(Account, pk=account_number)
        response = build_response(True, account_number, amount,
                                  'DEBIT', 'Transaction successful')
        if account.pin != pin:
            response['success'] = False
            response['message'] = "Invalid pin"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        if amount <= 0:
            response['success'] = False
            response['message'] = "Amount must be greater than 0"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        if account.balance < amount:
            response['success'] = False
            response['message'] = "Insufficient funds"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        balance = account.balance
        balance -= amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        Transaction.objects.create(
            account=account,
            amount=amount,
            transaction_type='DEB'
        )
        return Response(data=response, status=status.HTTP_200_OK)


def build_response(success: bool, account_number, amount, transaction_type: str, message: str):
    response = {'request_time': datetime.datetime.now(),
                'success': success,
                'account_number': account_number,
                'amount': amount,
                'transaction_type': transaction_type,
                'message': message}
    return response

# class CreateAccount(CreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountCreateSerializer
