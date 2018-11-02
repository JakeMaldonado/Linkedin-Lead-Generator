'''
Basic request functions for requests
'''

import requests
import json
import time


def get_json(url):
    '''
    makes a get request and returns response json as dict
    :url : the url to make the request from
    :return info: the info returned by the response
    '''
    retries = 5
    while not retries == 0:
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return {"error": r.status_code}
            return json.loads(r.text)
        except:
            print('Connection refused.....')
            print('Sleeping for 5s before retrying.')
            time.sleep(5)
            print('Retrying')
            retries -= 1
    return None


def post_json(url, post=None, headers=None):
    '''
    posts data and returns the dictionary
    :url : the url to make the request
    :return info: response text 
    '''
    retries = 2
    while not retries == 0:
        try:
            r = requests.post(url, data=post, headers=headers)
            if r.status_code != 200:
                return {"error": r.status_code}
            return json.loads(r.text)
        except:
            print('Connection refused.....')
            print('Sleeping for 5s before retrying.')
            time.sleep(5)
            print('Retrying')
            retries -= 1
    return None


def put_json(url, put=None, headers=None):
    '''
    makes a PUT request and returns JSON as a dict
    :param url: url to PUT to
    :param put: data to PUT
    :param headers: headers to send
    :return:
    '''
    retries = 5
    while not retries == 0:
        try:
            if headers is None:
                headers = {"content-type": "application/json"}

            r = requests.put(url, data=put, headers=headers)

            if r.status_code != 200:
                return {'error': r.status_code}

            return json.loads(r.text)
        except:
            print('Connection refused.....')
            print('Sleeping for 5s before retrying.')
            time.sleep(5)
            print('Retrying')
            retries -= 1
    return None


def delete_json(url):
    '''
    makes a delete request and returns response json as dict
    :url : the url to make the request from
    :return info: the info returned by the response
    '''
    retries = 5
    while not retries == 0:
        try:
            r = requests.delete(url)
            if r.status_code != 200:
                return {"error": r.status_code}
            return json.loads(r.text)
        except:
            print('Connection refused.....')
            print('Sleeping for 5s before retrying.')
            time.sleep(5)
            print('Retrying')
            retries -= 1
    return None

