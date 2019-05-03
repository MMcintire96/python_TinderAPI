import json

import requests

from tinder_api.utils import config


def get(url):
    full_url = config.host + url
    r = requests.get(full_url, headers=config.headers)
    return r.json()

def post(url, p_data):
    full_url = config.host + url
    r = requests.post(full_url, headers=config.headers,
            data=json.dumps(p_data))
    return r.json()

def delete(url):
    full_url = config.host + url
    r = requests.delete(full_url, headers=config.headers)
    return r

def put(url, p_data):
    full_url = config.host + url
    r = requests.put(full_url, headers=config.headers,
            data=json.dumps(p_data))
    return r


if __name__ == '__main__':
    pass
