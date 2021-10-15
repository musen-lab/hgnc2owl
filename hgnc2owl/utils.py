"""Basic utilities module"""
import requests


def request_get(url, api_key):
    """
    Performs a get request that provides a (somewhat) useful error message.
    """
    try:
        headers = {
            'Authorization': 'apiKey ' + api_key
        }
        response = requests.get(url, headers=headers)
    except ImportError:
        raise ImportError("Couldn't retrieve the data, check your URL")
    else:
        return response


def request_delete(url, api_key):
    """
    Performs a delete request.
    """
    try:
        headers = {
            'Authorization': 'apiKey ' + api_key
        }
        response = requests.delete(url, headers=headers)
    except ImportError:
        raise ImportError("Couldn't delete the data, check your URL")
    else:
        return response


def json_handler(url, api_key):
    """Returns request in JSON (dict) format"""
    return request_get(url, api_key).json()
