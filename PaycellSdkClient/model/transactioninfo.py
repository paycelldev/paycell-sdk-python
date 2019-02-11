from django.db import models

class TransactionInfo(models.Model):
    transaction_id = models.CharField(max_length=255)
    transaction_date = models.CharField(max_length=255)