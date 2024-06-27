from django.conf import settings
from django.db import models
from .utils import generate_account_number
from .validators import validate_pin


# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1)
    account_number = models.CharField(max_length=10, default=generate_account_number,
                                      unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pin = models.CharField(max_length=4, validators=[validate_pin])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ACCOUNT_TYPE = [
        ('SAV', 'SAVINGS',),
        ('CUR', 'CURRENT'),
        ('DOM', 'DOMICILIARY'),
    ]
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPE, default='SAV')

    # def __str__(self):
    #     return f'Account: {self.first_name} {self.last_name} {self.account_type} {self.balance}'


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('DEB', 'DEBIT'),
        ('CRE', 'CREDIT'),
        ('TRAN_OUT', 'TRANSFER_OUT'),
        ('TRAN_IN', 'TRANSFER_IN'),
    ]
    TRANSACTION_STATUS = [
        ('P', 'PENDING',),
        ('S', 'SUCCESSFUL'),
        ('F', 'FAILED'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=8, choices=TRANSACTION_TYPE, default='CRE')
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS, default='S')
