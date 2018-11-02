from request_utilities import get_json, post_json, put_json, delete_json
from credentials import KINDLING_API_KEY
from json import loads, dumps
import get_email_format


KINDLING_URL = 'https://agile-beyond-80033.herokuapp.com/'


def post_user(user):
    '''
    posts a users information to the database
    :param user: contact info in dictionary
    :return contact: on success the server returns the contact object created
    '''
    url = KINDLING_URL + 'user/' + KINDLING_API_KEY
    res = post_json(url, post=user)
    print(res)
    return res


def delete_user(user):
    '''
    deletes a user form the kindling database
    :param user: user to delete from the db - only email is required in dict
    :return user: returns the user who was deleted from the db
    '''
    url = KINDLING_URL + 'user/' + user['email'] + '/' + KINDLING_API_KEY
    res = delete_json(url)
    print(res)
    return res


def get_user(user):
    '''
    gets a users information from the kindlong DB
    :param user: the user to get information for - only email is required
    :return user: returns the user object from DB on success
    '''
    url = KINDLING_URL + 'user/' + user['email'] + '/' + KINDLING_API_KEY
    res = get_json(url)
    print(res)
    return res


def post_format(email_format):
    '''
    posts email format to kindling DB
    :param email_format: email format to post to DB
    :return format: returns the object created in the DB if successful
    '''
    url = KINDLING_URL + 'format/' + KINDLING_API_KEY
    res = post_json(url, post=email_format)
    print(res)
    return res


def get_format(email_format):
    '''
    gets a format from the kidnling DB
    :param email_format: the format to get as a dictionary - domain is only required field
    :return format: if successful the format object from the DB is returned
    '''
    url = KINDLING_URL + 'format/' + email_format['domain'] + '/' + KINDLING_API_KEY
    res = get_json(url)
    print(res)
    return res


def post_domain(domain):
    '''
    posts a new domains information to the DB
    :param domain: the domain to post to the DB
    :return domain: returns the domain object in the DB on success
    '''
    url = KINDLING_URL + 'domain/' + KINDLING_API_KEY
    res = post_json(url, post=domain)
    print(res)
    return res


def get_domain(domain):
    '''
    gets a domains information from the kindling DB
    :param domain: the domain to get information on
    :return domain: the domain object stored in the DB on success
    '''
    url = KINDLING_URL + 'domain/' + domain['domain'] + '/' + KINDLING_API_KEY
    res = get_json(url)
    print(res)
    return res


def post_lead(lead):
    '''
    posts a lead to the kindling DB
    :param lead: lead to add to the DB
    :return lead: the lead object created in the DB on success
    '''
    url = KINDLING_URL + 'lead/' + KINDLING_API_KEY
    res = post_json(url, post=lead)
    print(res)
    return res


def get_lead(lead):
    '''
    Gets a lead from the kindling DB
    :param lead: the lead to get from the DB - email is all that is required
    :return lead: returns the lead object from the DB
    '''
    url = KINDLING_URL + 'lead/' + lead['email'] + '/' + KINDLING_API_KEY
    res = get_json(url)
    print(res)
    return res
