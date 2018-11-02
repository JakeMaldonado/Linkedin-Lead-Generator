'''
Request functions for hunter.io's API
'''

from request_utilities import get_json, post_json
from credentials import HUNTER_API_KEY

BASE_URL = 'https://api.hunter.io/v2/'


def domain_search(domain):
    '''
    does a hunter API domain search
    :param domain: domain to search
    :return: hunter response data
    '''
    url = '{}domain-search?domain={}&api_key={}'.format(BASE_URL, domain, HUNTER_API_KEY)
    return get_json(url)


def company_search(company):
    '''
    Searches a company for data on hunter
    :return: hunter response data
    '''
    url = '{}domain-search?company={}&api_key={}'.format(BASE_URL, company, HUNTER_API_KEY)
    return get_json(url)


def get_domain_pattern(domain):
    '''
    gets a domain email pattern from hunter
    :param domain: the domain to search for
    :return pattern: returns the domain pattern
    '''
    r = domain_search(domain)
    if 'error' in r:
        return r
    return r['data']['pattern']


def find_person_at_company(first_name, last_name, company):
    '''
    finds a persons email by company
    :param first_name: first name of contact to find
    :param last_name: last name of contact to find
    :param company: company the contact works at
    :return: email of the person
    '''
    url = '{}email-finder?company={}&first_name={}&last_name={}&api_key={}'.format(BASE_URL, company, first_name,
                                                                                   last_name, HUNTER_API_KEY)
    r = get_json(url)
    if 'error' in r:
        return r
    return r['data']['email']


def find_person_at_domain(first_name, last_name, domain):
    '''
    finds a persons email data by domain
    :param first_name: first name of contact to find
    :param last_name: last name of contact to find
    :param domain: domain of the company the contact works at
    :return: email data of the person
    '''
    url = '{}email-finder?domain={}&first_name={}&last_name={}&api_key={}'.format(BASE_URL, domain, first_name,
                                                                                  last_name, HUNTER_API_KEY)
    r = get_json(url)
    if 'error' in r:
        return None
    if r['data']['email'] is not None:
        return r['data']
    return None


def find_contact_email(first_name, last_name, domain):
    '''
    finds a persons email by domain
    :param first_name: first name of contact to find
    :param last_name: last name of contact to find
    :param domain: domain of the company the contact works at
    :return: email of the person
    '''
    r = find_person_at_domain(first_name, last_name, domain)
    if r is not None and 'error' not in r:
        return r['email']
    return None

