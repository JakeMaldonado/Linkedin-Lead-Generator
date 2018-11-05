'''
Complete Scrape Class
'''
from hubspot_utilities import company_domain_search, upload_company, update_company_format, get_format_from_domain_search
from hunter_utilities import find_person_at_domain, find_contact_email
from selenium_utilities import linkedin_account_scrape, linkedin_scrape, google_company_search, get_driver, linkedin_nav_headcount_scrape, linkedin_like_post, linkedin_account_domain, auto_connect

from credentials import POD_ACCOUNTS

from gmail_utilities import is_gmail
from get_email_format import get_email_format, format_email
from tech_lookup import tech_lookup
import kindling_api as k_api


class GenerateLeads:
    def __init__(self, url, location):
        self.url = url
        self.location = location

    def scrape(self):
        '''
        scrapes the url for all linkedin data
        :return: returns the scrape data
        '''
        return linkedin_scrape(self.url)
    
    def find_contact_domains(self, contacts):
        '''
        finds the company domains for a list of contacts
        :param contacts: contacts from a linkedin scrape
        :return contacts_updated: contacts with domains
        '''

        found = {}

        driver = get_driver(True)
        clean_contacts = {'contacts': []}

        while not contacts['contacts'] == []:
            contact = contacts['contacts'].pop()

            if contact['company'] in found:
                domain = found[contact['company']]
            else:
                domain = google_company_search(self.location, contact['company'], driver)
                if domain is not None:
                    found[contact['company']] = domain

            if domain is not None and is_gmail('@' + domain):
                contact['domain'] = domain
                clean_contacts['contacts'].append(contact)
        return clean_contacts

    def find_emails(self, contacts):
        '''
        finds contact emails if they exist
        :param contacts: contacts to find emails for
        :return complete_contacts: completed contacts with emails on gmail
        '''
        completed_contacts = {'contacts': []}

        while not contacts['contacts'] == []:
            contact = contacts['contacts'].pop()
            print(contact)
            hubspot_search = company_domain_search(contact['domain'])
            if hubspot_search is None:
                email = find_contact_email(contact['first_name'], contact['last_name'], contact['domain'])
                if email is not None:
                    email_format = get_email_format(contact['first_name'], contact['last_name'], email)
                    print(email_format)
                    if email_format is not None:
                        upload_company(contact['company'], contact['domain'], email_format)
                        contact['email'] = email
                        print('Added {} to contacts'.format(email))
                        completed_contacts['contacts'].append(contact)
                
            else:
                hubspot_format = get_format_from_domain_search(hubspot_search)
                print(hubspot_format)
                if hubspot_format is not None:
                    email = format_email(contact['first_name'], contact['last_name'], contact['domain'], hubspot_format)
                    print(email)
                    if email is not None:
                        contact['email'] = email
                        print('Added {} to contacts'.format(email))
                        completed_contacts['contacts'].append(contact)

                else:
                    email = find_contact_email(contact['first_name'], contact['last_name'], contact['domain'])
                    print(email)
                    if email is not None:
                        email_format = get_email_format(contact['first_name'], contact['last_name'], email)
                        print(email_format)
                        if email_format is not None:
                            company_id = hubspot_search['results'][0]['companyId']
                            update_company_format(email_format, company_id)
                            contact['email'] = email
                            print('Added {} to contacts'.format(email))
                            completed_contacts['contacts'].append(contact)

        return completed_contacts


class GenerateKindling:
    def __init__(self, url, location, tech_keys=None):
        self.url = url
        self.location = location
        self.tech_keys = tech_keys

    def scrape(self):
        '''
        scrapes the url for all linkedin data
        :return: returns the scrape data
        '''
        return linkedin_scrape(self.url)

    def find_contact_domains(self, contacts):
        '''
        finds the company domains for a list of contacts
        :param contacts: contacts from a linkedin scrape
        :return contacts_updated: contacts with domains
        '''

        found = {}

        driver = get_driver(True)
        clean_contacts = {'contacts': []}

        while not contacts['contacts'] == []:
            contact = contacts['contacts'].pop()
            try:
                if contact['company'] in found:
                    domain = found[contact['company']]
                else:
                    domain = google_company_search(self.location, contact['company'], driver)
                    if domain is not None:
                        found[contact['company']] = domain

                if domain is not None:
                    contact['domain'] = domain
                    clean_contacts['contacts'].append(contact)
            except Exception as e:
                print('Some Error occurred - skipping contact: ')
                print(e)
                print(contact)
        return clean_contacts

    def find_emails(self, contacts):
        '''
        finds contact emails if they exist - uses a lot of hunter requests
        // Im working on a better system for this
        :param contacts: contacts to find emails for
        :return complete_contacts: completed contact
        '''
        completed_contacts = {'contacts': []}

        while not contacts['contacts'] == []:
            contact = contacts['contacts'].pop()
            print(contact)

            # check kindling API
            res = k_api.get_format(contact)
            if res['doc']:
                # if in - format email
                email = format_email(contact['first'], contact['last'], contact['domain'], res['doc']['format'])
                if email:
                    contact['email'] = email
                    completed_contacts.append(contact)
                    res = k_api.post_lead(contact)
                    print(res)

            # if not - make a hunter request
            else:
                email = find_person_at_domain(first_name, last_name, domain)
                if email:
                    # add domain info and format
                    contact['email'] = email
                    email_format = {
                        'format': get_email_format(contact['first'], contact['last'], email),
                        'domain': contact['domain']
                    }
                    domain_info = {
                        'domain': contact['domain'],
                        'company': contact['company']
                    }
                    format_res = k_api.post_format(email_format)
                    domain_res = k_api.post_domain(domain_info)
                    lead_res = k_api.post_lead(contact)
                    print(format_res),
                    print(domain_res),
                    print(lead_res)

        return completed_contacts


    def find_tech(self, contacts):
        '''
        Searched for tech in contact domains - use before find emails
        to save hunter requests
        :param contacts: contacts to search
        :return: clean_contacts
        '''
        clean_contacts = {'contacts': []}

        while not contacts['contacts'] == []:
            contact = contacts['contacts'].pop()
            print('sending:')
            print(contact)
            has_tech = tech_lookup(contact['domain'], self.tech_keys)
            print(contact['domain'])
            print(has_tech)
            if has_tech:
                clean_contacts['contacts'].append(contact)

        return clean_contacts

    def note_tech(self, contacts):
        '''
        Will note if contact has tech. Does not delete them like find_tech()
        :return clean_contacts: contacts noted if they have the tech
        '''
        clean_contacts = {'contacts': []}

        while not contacts['contacts'] == []:
            contact = contacts['contacts'].pop()
            print('sending:')
            print(contact)
            has_tech = tech_lookup(contact['domain'], self.tech_keys)
            print(contact['domain'])
            print(has_tech)
            contact['has_tech'] = has_tech
            clean_contacts['contacts'].append(contact)
        return clean_contacts


class GenerateAccounts:
    def __init__(self, url, tech_keys=None):
        self.url = url
        self.tech_keys = tech_keys
        self.accounts = None

    def scrape(self):
        '''
        scrapes the url for all linkedin data
        :return: returns the scrape data
        '''
        return linkedin_account_scrape(self.url)

    def headcount_scrape(self, accounts):
        '''
        scrapes headcount from account profile links in a csv
        :return:
        '''
        self.accounts = linkedin_nav_headcount_scrape(accounts)
        return self.accounts

    def company_domain_scrape(self):
        self.accounts = linkedin_account_domain(self.accounts)
        return self.accounts


class LinkedInPod:
    def __init__(self, url):
        self.accounts = POD_ACCOUNTS
        self.current_user = None
        self.url = url

    def like_post(self):
        '''
        Like posts from each account in accounts stored in credentials.py
        :return:
        '''
        print('\n\n-- Liking LinkedIn Post --\n\n')
        while self.accounts:
            account = self.accounts.pop()
            print('\nLiking with user:')
            print(account)
            linkedin_like_post(self.url, account)

    def engage(self):
        '''
        likes and comments on post provided using each account stored in credentials.py
        :return:
        '''
        while self.accounts:
            account = self.accounts.pop()


class KindlingMain:
    def __init__(self, url):
        self.url = url
        self.driver = get_driver(True)

    def options_interface(self):
        print('\n\n---- STARTED KINDLING ----\n\n')
        option = input('\n--- OPTIONS ---\n\n 1 - Lead Scrape\n 2 - Lead Scrape')


class AutoConnect:
    def __init__(self, contact_data):
        self.contacts = contact_data

    def massConnect(self):
        driver = get_driver(True)
        print('\n\n --- Auto-Connector Started --- \n\n')
        auto_connect(driver, self.contacts)

