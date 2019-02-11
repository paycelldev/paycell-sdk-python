from .utils import constants
import uuid
from .model.installmentplan import InstallmentPlan
from .model.metadata import Metadata
from .model.payment import Payment

"""
    This functions are used as model constructors    
"""
def create_installmentplan(payment, id, amount, cardbrand, payment_type, count):
    installment = InstallmentPlan()
    installment.payment = payment
    installment.count = count
    installment.amount = amount
    installment.card_brand = cardbrand
    installment.line_id = id
    installment.payment_method_type = payment_type
    return installment

def create_payment(payment_security, currency, amount):
    payment = Payment()
    payment.payment_security = payment_security
    payment.payment_reference_number = 'T-' + str(uuid.uuid4())
    payment.currency = currency
    payment.amount = amount
    payment.status = 0
    return payment


def create_metadata(host_account, language, msisdn, ip, payment):
    metadata = Metadata()
    metadata.application_name = constants.APPLICATION_NAME
    metadata.terminal_code = constants.TERMINAL_CODE
    metadata.merchant_code = constants.MERCHANT_CODE
    metadata.host_account = host_account
    metadata.language = language
    metadata.msisdn = msisdn
    metadata.client_ip_address = ip
    metadata.payment = payment
    return metadata

