from django.db import models
from .payment import Payment


class Metadata(models.Model):
    application_name = models.CharField(max_length=255)
    merchant_code = models.CharField(max_length=255)
    terminal_code = models.CharField(max_length=255)
    host_account = models.CharField(max_length=255)
    msisdn = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    client_ip_address = models.CharField(max_length=255)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)