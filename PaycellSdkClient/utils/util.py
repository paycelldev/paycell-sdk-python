import hashlib
import base64


# hashes strings in a given list then returns the result in iso-8859 format
def digest_list(message_list):
    m = hashlib.sha256()
    for message in message_list:
        m.update(str(message).encode('utf-8'))
    return base64.b64encode(m.digest()).decode('iso-8859-1')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
