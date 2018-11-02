from get_email_format import get_email_format
from credentials import KINDLING_API_KEY
from request_utilities import post_json
from itertools import cycle

from lxml.html import fromstring
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import csv


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

print(get_proxies())


def csv_to_list(csv_name):
    '''
    turns a csv into an array
    :param csv_name: the csv to turn into a list
    :return list: the list being returned
    '''
    with open(csv_name, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        data.pop(0)
        print(data)
    return data


def lead_csv_to_db(csv_name):
    '''
    Imports lead info to the DB
    :param csv_name: the name of the csv to import
    :return status: status of how the import went
    '''
    list_data = csv_to_list(csv_name)
    while list_data:
        contact = list_data.pop()
        email_format = get_email_format(contact[0], contact[1], contact[6])

        if email_format:
            format_res = post_json('https://agile-beyond-80033.herokuapp.com/format/' + KINDLING_API_KEY, post={
                "company": contact[2],
                "domain": contact[4],
                "format": email_format
            })
            print('Uploaded Format:')
            print(format_res)
            sleep(0.4)

        lead = {
            "first": contact[0],
            "last": contact[1],
            "company": contact[2],
            "title": contact[3],
            "domain": contact[4],
            "location": contact[5],
            "email": contact[6]
        }
        lead_res = post_json('https://agile-beyond-80033.herokuapp.com/lead/' + KINDLING_API_KEY, post=lead)
        print('\nUploaded Lead:')
        print(lead_res)
        print()
        sleep(0.4)
    return 'success'


def find_contact_email(url):
    '''
    Finds the mailto on a website and returns the email
    :param url: url to search
    :return email: email found or empty list
    '''
    possible_paths = ['', '/contact', '/contact-us', '/contact-us.html', '/contact.html']
    found = False
    while possible_paths and not found:
        path = possible_paths.pop(0)
        path_url = url + path
        if 'http' not in path_url and 'https' not in path_url:
            print(url)
            path_url = 'http://' + path_url
        try:
            print('\nChecking:')
            print(path_url)
            res = requests.get(path_url)
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', res.text)
            if not emails == []:
                found = True
            print(emails)
        except Exception as e:
            print('\nError in find contact email: ')
            print(e)
    if emails:
        return emails
    else:
        return []


def csv_yelp_domain_scrape(csv_name):
    '''
    Scrapes the domains from yelp pages
    :param csv_name: csv with yelp domains
    :return with domains: returns the csv contracts with the domains as a 2d list
    '''
    list_data = csv_to_list(csv_name)
    list_data.pop(0)
    new_contacts = []
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    while list_data:
        if not proxies:
            proxies = get_proxies()
        lead = list_data.pop()
        yelp_domain = lead.pop(0)
        print('\n\nLead Domain:')
        print(yelp_domain)
        retries = 3
        finished = False
        while retries and not finished:
            try:
                proxy = next(proxy_pool)
                print('Using proxy IP:')
                print(proxy)
                page = requests.get(yelp_domain, proxies={"http": proxy, "https": proxy})
                soup = BeautifulSoup(page.text, 'html.parser')
                domains = soup.find_all(class_='biz-website js-biz-website js-add-url-tagging')
                if domains:
                    domain_element = domains[0].text
                    domain = domain_element.split('\n')[2]
                    lead.append(domain)
                    new_contacts.append(lead)
                    print('Adding Lead: ')
                    print(lead)
                    # emails = find_contact_email(domain)
                    # if emails:
                    #     lead.append(emails[0])
                    #     new_contacts.append(lead)
                sleep(2)
                finished = True
                retries -= 1
            except Exception as e:
                print('\nError in yelp domain scrape:')
                print(e)
                sleep(2)
                retries -= 1
    return new_contacts


def lead_domain_get_email_from_csv(csv_name):
    '''
    Finds contacts website email from contact domains
    :param csv_name: csv file to search for and take data from
    :return completed_contacts: leads with emails in a list
    '''
    list_data = csv_to_list(csv_name)
    list_data.pop(0)
    new_contacts = []
    while list_data:
        try:
            lead = list_data.pop()
            print('\n\n----------------------\nChecking lead: ')
            print(lead)
            domain = lead[len(lead) - 1]
            emails = find_contact_email(domain)
            if emails:
                print('Emails found: ')
                print(emails)
                lead.append(emails[0])
                new_contacts.append(lead)
                print('Adding contact to CSV: ')
                print(lead)
        except Exception as e:
            print('\nError Occurred: ')
            print(e)
    return new_contacts


def array_to_csv(array, file_name):
    '''
    Saves a 2D array to a csv file
    :param array: The array to save as a csv
    :param file_name: File to turn into an array
    :return status: If the array was saved as a csv
    '''
    try:
        if '.csv' not in file_name:
            file_name = file_name + '.csv'
        with open(file_name, "w+") as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(array)
        return 'Success!'
    except Exception as e:
        print('Error in array to CSV: ')
        print(e)
        return 'Error'


leads_with_email = csv_yelp_domain_scrape('yelpScrape.csv')
print(leads_with_email)
array_to_csv(leads_with_email, 'leads.csv')


# leads_with_email = lead_domain_get_email_from_csv('leads.csv')
# print(leads_with_email)
# array_to_csv(leads_with_email, 'email_leads.csv')