'''
functions for checking gmail
'''

import dns.resolver
import re

email_host_regex = re.compile(".*@(.*)$")
gmail_servers_regex = re.compile("(.google.com.|.googlemail.com.)$", re.IGNORECASE)


def is_gmail(email):
    '''
    Description: Checks if a domain or
    email address is hosted on Gmail
    -------------------------------------
    :param email: The email which should
    be checked
    :return: returns a bool either True
    or False if the email is Gmail it
    it will return True
    -------------------------------------
    Use: x = is_gmail(email)
    '''
    m = email_host_regex.findall(email)
    try:
        if m and len(m) > 0:
            host = m[0]
            if host and host != '':
                host = host.lower()
    
            if host == "gmail.com":
                return True
            else:
                answers = dns.resolver.query(host, 'MX')
                for rdata in answers:
                    m = gmail_servers_regex.findall(str(rdata.exchange))
                    if m and len(m) > 0:
                        return True
    except Exception:
        return False

    return False
