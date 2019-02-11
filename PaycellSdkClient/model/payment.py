from django.db import models


class Payment(models.Model):
    amount = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    payment_reference_number = models.CharField(max_length=255)
    payment_security = models.CharField(max_length=255)
    status = models.IntegerField(default=0)  # 0 -> unpaid, 1-> paid, 2->cancelled
