from django.test import TestCase

from .models import create_installmentplan, create_metadata, create_payment, Payment, InstallmentPlan, Metadata
from .services.paymentservice import PaymentService
from unittest import skip


# This class tests only init method, in order to reverse or refund, transaction must be completed
class PaycellSDK(TestCase):
    def setUp(self):
        payment = create_payment("NON_THREED_SECURE", "99", "100")
        payment.payment_reference_number = "T-a05468b8-b3f7-4afc-9c97-0bfd3384c7e0"
        payment.save()
        metadata = create_metadata("xxx@xxx.com", "tr", "905465553333", "10.252.121.69", payment)
        metadata.save()
        installmentplan = create_installmentplan(payment, "1", "100", "BONUS", "CREDIT_CARD", "1")
        installmentplan.save()

    def test_init_payment(self):
        payment_service = PaymentService()
        payment = Payment.objects.get(payment_reference_number="T-a05468b8-b3f7-4afc-9c97-0bfd3384c7e0")
        installmentplan = InstallmentPlan.objects.get(payment=payment)
        metadata = Metadata.objects.get(payment=payment)
        response = payment_service.init_payment(metadata, payment, [installmentplan])
        self.assertEqual(response["statusCode"], str(0))

    # Following three cases need a reference_number for a completed transaction
    @skip
    def test_query_status(self):
        payment_service = PaymentService()
        payment = Payment.objects.get(payment_reference_number="T-a05468b8-b3f7-4afc-9c97-0bfd3384c7e0")
        metadata = Metadata.objects.get(payment=payment)
        response = payment_service.status_query(metadata, payment)
        self.assertEqual(response["responseHeader"]["statusCode"], str(0))

    @skip
    def test_refund_payment(self):
        payment_service = PaymentService()
        payment = Payment.objects.get(payment_reference_number="T-a05468b8-b3f7-4afc-9c97-0bfd3384c7e0")
        metadata = Metadata.objects.get(payment=payment)
        response = payment_service.refund_payment(metadata, payment, 50)
        self.assertEqual(response["responseHeader"]["statusCode"], str(0))

    @skip
    def test_cancel_payment(self):
        payment_service = PaymentService()
        payment = Payment.objects.get(payment_reference_number="T-a05468b8-b3f7-4afc-9c97-0bfd3384c7e0")
        metadata = Metadata.objects.get(payment=payment)
        response = payment_service.cancel_payment(metadata, payment)
        self.assertEqual(response["responseHeader"]["statusCode"], str(0))


