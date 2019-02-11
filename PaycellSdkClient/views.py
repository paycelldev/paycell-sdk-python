from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from .services.paymentservice import PaymentService
from .models import create_installmentplan, create_payment, create_metadata, Payment, InstallmentPlan, Metadata
from django.views.decorators.csrf import csrf_exempt
from .utils import constants as constants
from .utils.util import get_client_ip
import json

def index(request):
    if request.method == 'GET':
        return render(request, 'init.html')

#   Gets the necessary information from post request body that is sent from front-end
#   Creates payment, metadata, installmentPlan objects and saves them to db
#   returns trackingUrl and ref number
def init(request):
    if request.method == 'GET':
        return render(request, 'init.html')
    elif request.method == 'POST':
        data = json.loads(request.POST['data'])
        payment = create_payment(data["paymentsecurity"], data["currency"], data["amount"])
        payment.save()
        metadata = create_metadata(data["hostaccount"], data["language"], data["msisdn"], get_client_ip(request), payment)
        metadata.save()

        installments = []
        for install in data['installments']:
            installment = create_installmentplan(payment, install['id'], install['amount'], install['cardBrand'], install['paymentMethod'], install['count'])
            installment.save()
            installments.append(installment)

        payment_service = PaymentService()
        init_response = payment_service.init_payment(metadata, payment, installments, request.get_host())
        if int(init_response["statusCode"]) == constants.RESULT_CODE_SUCCESS:
            trackurl = constants.VALIDATION_TRACKING_URL + init_response['trackingId']
            return HttpResponse(json.dumps({'trackingUrl': trackurl, 'paymentReferenceNumber': payment.payment_reference_number}), content_type='application/json')
        else:
            response = HttpResponse(json.dumps(init_response), content_type='application/json')
            response.status_code = 400
            return response


# this method is called after a transaction is done,
# request is made by sdk including the result of the payment
# here it finds the payment object and updates it status accordingly
@csrf_exempt
def handle_post_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            payment = Payment.objects.get(payment_reference_number= data["paymentReferenceNumber"])
            if data["isReverse"]:
                payment.status = 2
            else:
                payment.status = 1
            payment.save()
            installments = []
            for installment in InstallmentPlan.objects.filter(payment=payment):
                installments.append(model_to_dict(installment))
            response = {
                "payment": model_to_dict(payment),
                "installments": installments
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        except Payment.DoesNotExist:
            return HttpResponse(json.dumps({"error": "Invalid paymentReferenceNumber"}), content_type='application/json')


#
#   This endpoint is used to check status of a payment
#   It accepts payment ref number as url parameter
#   Right now, after the payment is done, browser redirects to this endpoint
#   because it has given as return url into init request
#
def check_status(request, payment_reference_number):
    if request.method == 'GET':
        payment = Payment.objects.get(payment_reference_number=payment_reference_number)
        metadata = Metadata.objects.get(payment=payment)
        payment_service = PaymentService()
        response = payment_service.status_query(metadata, payment)
        return render(request, 'checkstatus.html', response)

#
# This end point is used to cancel or reverse the payment
# It accepts a post request with paymentReferenceNumber
#
def reverse_payment(request):
    if request.method == 'POST':
        data = request.POST.dict()
        payment = Payment.objects.get(payment_reference_number=data["paymentReferenceNumber"])
        metadata = Metadata.objects.get(payment=payment)

        payment_service = PaymentService()
        response = payment_service.cancel_payment(metadata, payment)
        return HttpResponse(json.dumps(response), content_type='application/json')

#
# This end point is used to refund the payment
# It accepts a post request with paymentReferenceNumber and refundAmounte
#
def refund_payment(request):
    if request.method == 'POST':
        data = request.POST.dict()
        payment = Payment.objects.get(payment_reference_number=data["paymentReferenceNumber"])
        metadata = Metadata.objects.get(payment=payment)
        payment_service = PaymentService()
        response = payment_service.refund_payment(metadata, payment, data["refundAmount"])
        return HttpResponse(json.dumps(response), content_type='application/json')



