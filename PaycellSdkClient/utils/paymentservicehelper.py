from ..utils.constants import APPLICATION_PASSWORD, APPLICATION_NAME, SECURE_CODE, RETURN_URL, POST_RESULT_URL
from datetime import datetime
from ..utils.util import digest_list
import random
import uuid
import socket

"""
    This class is a helper to create related request dicts
    functions can also be implemented as static
"""



class PaymentHelper(object):
    def __init__(self):
        pass

    def create_status_query_request(self, metadata, payment):
        request = {
            "requestHeader": self.create_request_header(metadata),
            "merchantCode": metadata.merchant_code,
            "originalPaymentReferenceNumber": payment.payment_reference_number
        }
        return request

    def create_refund_request(self, metadata, payment, refund_amount):
        request = {
            "requestHeader": self.create_request_header(metadata),
            "merchantCode": metadata.merchant_code,
            "msisdn": metadata.msisdn,
            "originalReferenceNumber": payment.payment_reference_number,
            "referenceNumber": 'T-' + str(uuid.uuid4()),
            "amount": refund_amount
        }
        return request

    def create_reverse_request(self, metadata, payment):
        request = {
            "requestHeader": self.create_request_header(metadata),
            "merchantCode": metadata.merchant_code,
            "msisdn": metadata.msisdn,
            "originalReferenceNumber": payment.payment_reference_number,
            "referenceNumber": 'T-' + str(uuid.uuid4()),
        }
        return request

    # when this app is deployed to a server, server_address variable can be changed with server's url
    def create_init_request(self, metadata, payment, installments, server_address):
        request = {
            "requestHeader": self.create_init_request_header(metadata),
            "payment": self.create_payment_dict(payment, installments),
            "hashData": self.create_hash_data(metadata, payment, installments),
            "hostAccount": metadata.host_account,
            "language": metadata.language,
            "returnUrl": server_address + RETURN_URL + payment.payment_reference_number,
            "postResultUrl": server_address + POST_RESULT_URL,
            "timeoutDuration": str(300)
        }
        return request

    def create_request_header(self, metadata):
        return {
            "transactionId": random.randrange(1000000000000000000, 99999999999999999999),
            "transactionDateTime": datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3],
            "clientIPAddress": metadata.client_ip_address,
            "applicationName": APPLICATION_NAME,
            "applicationPwd": APPLICATION_PASSWORD
        }

    def create_init_request_header(self, metadata):
        merchant = {
            "merchantCode": metadata.merchant_code,
            "terminalCode": metadata.terminal_code,
            # "logos": null
        }

        transaction_info = {
            "transactionDateTime": datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3],
            "transactionId": str(random.randrange(1000000000000000000, 99999999999999999999))
        }

        request_header = {
            "applicationName": APPLICATION_NAME,
            "applicationPassword": APPLICATION_PASSWORD,
            "merchant": merchant,
            "transactionInfo": transaction_info
        }
        return request_header

    def create_payment_dict(self, payment, installments):
        payment_dict = {
            "amount": payment.amount,
            "currency": payment.currency,
            "paymentReferenceNumber": payment.payment_reference_number,
            "paymentSecurity": payment.payment_security,
            "instalmentPlan": []
        }
        for installment in installments:
            installment_dict = {
                "lineId": installment.line_id,
                "paymentMethodType": installment.payment_method_type,
                "cardBrand": installment.card_brand,
                "count": installment.count,
                "amount": installment.amount
            }
            payment_dict["instalmentPlan"].append(installment_dict)
        return payment_dict

    """
    1- Security Data : Sha256(SecureCode + TerminalCode)
    2- Merchant Hash Data : Sha256(paymentReferenceNumber + terminalCode + amount + currency + paymentSecurity 
        + hostAccount + intallmentPlan (lineId sırası ile taksit bilgileri birleştirilir --> lineId 
        + paymentMethodType + cardBrand + count + amount) + SecurityData)
    """
    def create_hash_data(self, metadata, payment, installments):
        security_data = digest_list([SECURE_CODE, metadata.terminal_code])
        message_list = [payment.payment_reference_number, metadata.terminal_code, payment.amount, payment.currency,
                        payment.payment_security, metadata.host_account]

        """for installment in installments:
            message_list.append(installment.line_id)
            message_list.append(installment.payment_method_type)
            message_list.append(installment.card_brand)
            message_list.append(installment.count)
            message_list.append(installment.amount)"""
        message_list.append(security_data)
        return digest_list(message_list)
