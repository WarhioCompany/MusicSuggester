import requests
import json


base_header = {'Content-Type': 'application/json'}


def make_header(headers=None):
    new_header = base_header
    if headers:
        new_header = {**headers, **base_header}
    return new_header


def get_request(url, params, headers=None):
    data = requests.get(url=url, params=params, headers=headers)
    return json.loads(data.text)
