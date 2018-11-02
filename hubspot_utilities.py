'''
Various functions for hubspot API
'''

from request_utilities import get_json, post_json, put_json
from credentials import HUBSPOT_API_KEY
from json import dumps
from time import sleep

BASE_URL = 'https://api.hubapi.com/'


def company_domain_search(domain):
    '''
    searches hubspot companies for a domain
    :param domain: domain to search for
    :return: retuns the domain data
    '''
    headers = {"content-type": "application/json"}
    post_data = {
        "limit": 2,
        "requestOptions": {
            "properties": [
                "domain",
                "createdate",
                "name",
                "hs_lastmodifieddate"
            ]
        },
        "offset": {
            "isPrimary": True,
            "companyId": 0
        }
    }
    dump_data = dumps(post_data)
    url = '{}/companies/v2/domains/{}/companies?hapikey={}'.format(BASE_URL, domain, HUBSPOT_API_KEY)
    r = post_json(url, dump_data, headers)

    if 'error' in r:
        return None

    if r['results'] == []:
        return None

    return r


def company_exists(response):
    '''
    cyhecks if a domain search exists
    :param response: the response data from a domain search
    :return: bool - if company exists, True ? False
    '''
    print('RR:')
    print(response)
    if 'error' in response:
        return response
    elif not response['results'] == []:
        return True
    return False


def company_has_format(response):
    '''
    checks if there is a format in hubspot response
    :param response:
    :return: None if no format, format if found
    '''
    if 'error' in response:
        return response

    if 'format' in response:
        return response['results'][0]['properties']['format']['value']
    return None


def get_format_from_domain_search(response):
    '''
    gets a company by id from hubspot
    :param response: company to get
    :return: None or format if found
    '''
    exists = company_exists(response)
    if exists:
        company_id = response['results'][0]['companyId']
        url = '{}companies/v2/companies/{}?hapikey={}'.format(BASE_URL, company_id, HUBSPOT_API_KEY)

        r = get_json(url)
        email_format = company_has_format(r)

        if email_format is None:
            return None
        return email_format
    return None


def upload_company(name, domain, email_format=None):
    '''
    uploads a company to hubspot
    :param name: name of company
    :param domain: domain of company
    :param email_format: email format for company
    :return: status
    '''
    url = '{}/companies/v2/companies/?hapikey={}'.format(BASE_URL, HUBSPOT_API_KEY)
    headers = {"content-type": "application/json"}
    data = {
      "properties": [
        {
            "name": "name",
            "value": name
        },
        {
            "name": "domain",
            "value": domain
        },
        {
            "name": "format",
            "value": email_format
        }
      ]
    }
    data_dump = dumps(data)
    return post_json(url, data_dump, headers)


def update_company_format(email_format, company_id):
    '''
    updates a company's email format in hubspot
    :param email_format: the company email format
    :param company_id: the company id to fix
    :return:
    '''
    url = '{}/companies/v2/companies/{}?hapikey={}'.format(BASE_URL, company_id, HUBSPOT_API_KEY)
    headers = {"content-type": "application/json"}
    print(email_format)
    print(company_id)
    update_post_data = {
        "properties": [
            {
                "name": "format",
                "value": email_format
            }
        ]
    }
    data_dump = dumps(update_post_data)
    return put_json(url, data_dump, headers)


def get_contact_by_email(email):
    '''
    gets a contacts info from hubspot using their email
    :param email: email to search for
    :return contact_info:
    '''

    url = '{}contacts/v1/contact/email/{}/profile?hapikey={}'.format(BASE_URL, email, HUBSPOT_API_KEY)
    print(url)
    r = get_json(url)
    return r
