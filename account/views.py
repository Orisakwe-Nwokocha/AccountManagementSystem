from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Account, Transaction
from .serializers import AccountSerializer, AccountCreateSerializer


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
        account_number = request.data['account_number']
        amount = Decimal(request.data['amount'])
        account = get_object_or_404(Account, pk=account_number)
        if amount <= 0.0:
            return Response(data={"success": False, "message": "Amount must be greater than 0"},
                            status=status.HTTP_400_BAD_REQUEST)
        account.balance += amount
        account.save()
        Transaction.objects.create(
            account=account,
            amount=amount
        )
        return Response(data={"success": True, "message": "Transaction successful"}, status=status.HTTP_200_OK)


class Withdraw(APIView):
    @staticmethod
    def post(request):
        account_number = request.data['account_number']
        amount = Decimal(request.data['amount'])
        pin = request.data['pin']
        account = get_object_or_404(Account, pk=account_number)
        if account.pin != pin:
            return Response(data={"success": False, "message": "Invalid pin"}, status=status.HTTP_400_BAD_REQUEST)
        if amount <= 0:
            return Response(data={"success": False, "message": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        if account.balance < amount:
            return Response(data={"success": False, "message": "Insufficient funds"},
                            status=status.HTTP_400_BAD_REQUEST)
        account.balance -= amount
        account.save()
        Transaction.objects.create(
            account=account,
            amount=amount,
            transaction_type='DEB'
        )
        return Response(data={"success": True, "message": "Transaction successful"}, status=status.HTTP_200_OK)
