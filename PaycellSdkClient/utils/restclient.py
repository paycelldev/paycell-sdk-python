import json
import requests


class RestClient(object):
    def __init__(self):
        pass

    def make_post_request(self, url, body_dictionary, header_dictionary):
        return requests.post(url, data=json.dumps(body_dictionary), headers=header_dictionary)

    def make_get_request(self, url, body_dictionary):
        return requests.get(url, headers=body_dictionary)

