from selenium_utilities import url_email_scrape, get_driver
import requests
import json
import csv

with open('data.json') as f:
    data = json.load(f)
    data_list = data['data']

    domains = {"data": []}

    while data_list:
        new_field = data_list.pop()
        split_href = new_field['Field1'].split(' ')[1].split('%2F')
        url = split_href[len(split_href) - 2]
        domains['data'].append({"url": url})

    print(domains)
    # clean_domains = {
    #     "data": []
    # }
    # driver = get_driver(True)

    # while domains:
    #     url = domains.pop()
    #     # result = url_email_scrape(driver, url)
    #     if 'http' not in url and 'https' not in url:
    #         url = 'http://' + url
    #     res = requests.get(url)
    #     if result:
    #         clean_domains['data'].append({
    #             "domain": url,
    #             "email": result
    #         })

    toCSV = domains['data']
    if len(toCSV) > 0:
        keys = toCSV[0].keys()

        file_name = 'email_ouput.csv'
        with open(file_name, "w") as f:
                    w = csv.DictWriter(f, keys)
                    w.writeheader()
                    w.writerows(toCSV)

def get_company_url(contacts):
    '''
    goes to a yp link and gets the company domain
    :return clean_contacts: contacts with their domains corrected
    '''
    clean_contacts = []
    contacts.pop(0)
    while contacts:
        contact = contacts.pop()
        clean_url = requests.get(contact[3]).url
        clean_contacts.append(contact.append(clean_url))
    return clean_contacts

def get_company_email(domain):
    '''
    uses kindling API to scrape an email form a company domain contact page
    :param domain: the domain to check
    :return email: None if email not found
    '''
    return url_email_scrape(domain)
