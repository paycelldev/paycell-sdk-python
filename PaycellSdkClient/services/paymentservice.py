from ..utils.restclient import RestClient
from ..utils.constants import INIT_URL, REVERSE_URL, REFUND_URL, QUERY_STATUS_URL
from ..utils.paymentservicehelper import PaymentHelper

"""
This class makes the api calls, 
First calls helper class to create request objects according to the operation
Then makes the api calls and returns response dict
Functions can also be implemented as static 
"""
class PaymentService(object):
    def __init__(self):
        pass

    # installments param must be an array of installmentPlan objects
    def init_payment(self, metadata, payment, installments, server_ip):
        rest_client = RestClient()
        helper = PaymentHelper()
        body = helper.create_init_request(metadata, payment, installments, server_ip)
        response = rest_client.make_post_request(INIT_URL, body, {'content-type': 'application/json'})
        return response.json()

    def cancel_payment(self, metadata, payment):
        rest_client = RestClient()
        helper = PaymentHelper()
        body = helper.create_reverse_request(metadata, payment)
        response = rest_client.make_post_request(REVERSE_URL, body, {'content-type': 'application/json'})
        return response.json()

    def refund_payment(self, metadata, payment, refund_amount):
        rest_client = RestClient()
        helper = PaymentHelper()
        body = helper.create_refund_request(metadata, payment, refund_amount)
        response = rest_client.make_post_request(REFUND_URL, body, {'content-type': 'application/json'})
        return response.json()

    def status_query(self, metadata, payment):
        rest_client = RestClient()
        helper = PaymentHelper()
        body = helper.create_status_query_request(metadata, payment)
        response = rest_client.make_post_request(QUERY_STATUS_URL, body, {'content-type': 'application/json'})
        return response.json()