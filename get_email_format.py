'''
function for getting an email
'''


def get_email_format(first, last, email):
    '''
    get's the email format form someones email
    :param first_name: first name of contact
    :param last_name: last name of contact
    :param email: contacts email
    :return: returns the email format if found, if not found will return None
    '''
    username = email.split('@')[0]

    f = first.lower()
    l = last.lower()

    fi = f[0]
    li = l[0]

    sections_dict = {
        '{first}': f,
        '{last}': l,

        '{first}{last}': f + l,
        '{first}.{last}': f + '.' + l,
        '{first}_{last}': f + '_' + l,
        '{first}-{last}': f + '-' + l,

        '{last}{first}': f + l,
        '{last}.{first}': f + '.' + l,
        '{last}_{first}': f + '_' + l,
        '{last}-{first}': f + '-' + l,

        '{f}{last}': fi + l,
        '{f}.{last}': fi + '.' + l,
        '{f}_{last}': fi + '_' + l,
        '{l}{first}': li + f,
        '{last}{f}': l + fi
    }

    for email_format, user in sections_dict.items():
        if user == username:
            return email_format
    return None


def format_email(f, l, domain, email_format):
    '''
    formats an email from a known format and domain
    :param f: contact first name
    :param l: contact last name
    :param email_format: email format for domain
    :param domain: email domain
    :return: the formatted email address
    '''
    fi = f[0]
    li = l[0]

    sections_dict = {
        '{first}': f,
        '{last}': l,

        '{first}{last}': f + l,
        '{first}.{last}': f + '.' + l,
        '{first}_{last}': f + '_' + l,
        '{first}-{last}': f + '-' + l,

        '{last}{first}': f + l,
        '{last}.{first}': f + '.' + l,
        '{last}_{first}': f + '_' + l,
        '{last}-{first}': f + '-' + l,

        '{f}{last}': fi + l,
        '{f}.{last}': fi + '.' + l,
        '{f}_{last}': fi + '_' + l,
        '{l}{first}': li + f,
        '{last}{f}': l + fi
    }

    if email_format in sections_dict:
        username = sections_dict[email_format]
        email = username + '@' + domain
        return email

    return None

