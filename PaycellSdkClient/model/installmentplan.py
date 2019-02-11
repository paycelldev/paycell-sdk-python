from django.db import models
from .payment import Payment


class InstallmentPlan(models.Model):
    line_id = models.CharField(max_length=255)
    payment_method_type = models.CharField(max_length=255)
    card_brand = models.CharField(max_length=255)
    count = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


