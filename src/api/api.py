import requests

from src.const import REQUEST_URL



def req():
    try:
        response = requests.get(REQUEST_URL)
        return response
    except Exception as e:
        print(e)


def response_parse(response_object):
    print(response_object.content)


response_parse(req())
