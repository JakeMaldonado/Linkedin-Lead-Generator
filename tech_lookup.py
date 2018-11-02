from request_utilities import post_json
from json import dumps
from time import sleep


def tech_lookup(url, keys):
    '''
    Used to call tech lookup API
    :param url: the domain to check for the technology
    :param keys: the piece of code to look for in the page source - array
    :return: bool - if the code exists in the page
    '''
    check_url = 'https://tech-lookup.herokuapp.com/techSearch'
    headers = {"content-type": "application/json"}
    found = False
    try:
        data = {
            "url": url,
            "keys": keys
        }
        print('res sent')
        res = post_json(check_url, post=dumps(data), headers=headers)
        print(res)
        if res and res['result']:
            found = True
    except Exception:
        print('something went wrong calling page')
    return found

