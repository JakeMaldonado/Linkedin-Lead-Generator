'''
Functions for scraping using Selenium
'''

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

import tldextract

from credentials import LINKEDIN_USERNAME
from credentials import LINKEDIN_PASSWORD

import time


def send_word(word, location):
    '''
    sends keys to an element
    :param word: word to send
    :param location: element to send to
    :return:
    '''
    for letter in word:
        location.send_keys(letter)
        time.sleep(0.05)


def page_amount(result_amount):
    """
    Description: Calculates the number of
    pages there are for the search
    -------------------------------------
    :param result_amount: amount of
    results the page brings up
    :return pages: number of pages in the
    search
    -------------------------------------
    Use: v = page_amount(result_amount)
    """
    if ',' in result_amount or 'K' in result_amount or int(result_amount) > 1000:
        pages = 40
    elif int(result_amount) < 25:
        pages = 1
    else:
        pages = int(int(result_amount) / 25)
    return pages


def get_driver(max_screen):
    """
    Description: Gets a chrome driver
    session. User chooses if screen is
    maximized
    -------------------------------------
    :param max_screen: Boolean of if the
    chrome window should open maximized
    :return driver: and open chrome
    driver
    -------------------------------------
    Use: v = get_driver(max_screen)
    """
    if max_screen:
        options = webdriver.ChromeOptions()
        options.add_argument("--kiosk")
        driver = webdriver.Chrome(chrome_options=options)
        return driver
    elif not max_screen:
        driver = webdriver.Chrome()
        return driver
    else:
        print("parameter must be boolean")


def login(driver):
    '''
    logs into Linkedin from the login page
    :param driver: currently active chrome driver
    :return:
    '''
    driver.get("https://www.linkedin.com/")
    wait_for_element("login-email", driver, "class")
    login_user = driver.find_element_by_class_name("login-email")
    login_pass = driver.find_element_by_id("login-password")

    send_word(LINKEDIN_USERNAME, login_user)
    send_word(LINKEDIN_PASSWORD, login_pass)

    login_pass.send_keys(Keys.ENTER)

    return


def user_login(driver, user):
    '''
    logs into Linkedin from the login page
    :param driver: currently active chrome driver
    :param user: user to login as {"username": "example@example.com", "password": "password345"}
    :return:
    '''
    driver.get("https://www.linkedin.com/")
    wait_for_element("login-email", driver, "class")
    login_user = driver.find_element_by_class_name("login-email")
    login_pass = driver.find_element_by_id("login-password")

    send_word(user["username"], login_user)
    send_word(user["password"], login_pass)

    login_pass.send_keys(Keys.ENTER)

    return


def wait_for_element(element, driver, element_type):
    """
    Description: Will wait until the
    page has loaded the element before
    continuing
    -------------------------------------
    :param element: either a class name
    or id
    :param driver: the current driver
    :param element_type: either "class"
    or "id"
    :return:
    -------------------------------------
    Use: wait_for_element(element, driver, element_type)
    """
    if element_type == "class":
        try:
            myElem = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
        except TimeoutException:
            print("Loading for -- {} -- took too much time!".format(element))
    elif element_type == "id":
        try:
            myElem = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, element)))
        except TimeoutException:
            print("Loading for -- {} -- took too much time!".format(element))
    elif element_type == "selector":
        try:
            myElem = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
        except TimeoutException:
            print("Loading for -- {} -- took too much time!".format(element))
    else:
        print('Invalid type')
    return


def next_page(driver):
    '''
    clicks the next page button
    :param driver: the currently actvive chrome driver
    :return:
    '''
    next_page_class = 'search-results__pagination-next-button'
    wait_for_element(next_page_class, driver, 'class')

    next_page_button = driver.find_element_by_class_name(next_page_class)
    actions = ActionChains(driver)
    actions.move_to_element(next_page_button).perform()
    time.sleep(2)
    try:
        next_page_class = 'search-results__pagination-next-button'
        wait_for_element(next_page_class, driver, 'class')

        next_page_button = driver.find_element_by_class_name(next_page_class)
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).click().perform()
        time.sleep(4)
    except Exception as e:
        print(e)
    return


def get_pages_data(pages, driver):
    '''
    
    :param pages: 
    :param driver: 
    :return: 
    '''
    data = {
        'contacts': []
    }
    for page in range(pages):
        next_page_class = 'search-results__pagination-next-button'
        wait_for_element(next_page_class, driver, 'class')

        next_page_button = driver.find_element_by_class_name(next_page_class)
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).perform()
        time.sleep(3)
        next_page_button = driver.find_element_by_class_name(next_page_class)
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).perform()

        names = driver.find_elements_by_class_name("result-lockup")
        print('\n\nnames:')
        print(names)
        for element in names:
            try:
                profile_url_element = element.find_element_by_class_name("result-lockup__name")
                profile_url = profile_url_element.find_element_by_css_selector('a').get_attribute('href')
                name = profile_url_element.text
                company = element.find_element_by_class_name("result-lockup__position-company").text
                other_info = element.find_element_by_class_name("result-lockup__highlight-keyword").text
                contact = {
                    'name': name,
                    'company': company.split('\n')[0],
                    'other_info': other_info,
                    'profile_url': profile_url
                }
                print(contact)
                data['contacts'].append(contact)
            except Exception as e:
                print(e)
                pass

        try:
            wait_for_element(next_page_class, driver, 'class')

            next_page_button = driver.find_element_by_class_name(next_page_class)
            actions = ActionChains(driver)
            actions.move_to_element(next_page_button).click().perform()
            time.sleep(4)
        except Exception as e:
            print(e)

    return data


def find_name(full_name):
    '''
    finds first and last name from full name
    :param full_name: the full name to check
    :return : returns dict containing first and last name
    '''
    prefix_array = [
        'mc', 'van', 'von',
        'mac', 'fitz', 'o',
        'de', 'di', 'van de',
        'van der', 'van den',
        'da'
    ]

    remove_text = """"'!@#$%^&*()_+-={}|:"<>?[]\;',./'"""
    remove_array = [
        'MBA', 'CFA', 'CPA', 'HRPA',
        'CHRP', 'CPHR', 'PHD', 'CHRL',
        'CIPD', 'CHRP', 'jr', 'jr.',
        'JR', 'JR.', 'Jr', 'Jr.',
        'CCWP'
    ]

    first_check = full_name.split(',', 1)[0]
    split_name = first_check.split(" ")
    clean_words = []
    for word in split_name:
        word = word.split(',', 1)[0]
        if '.' not in word:
            for char in remove_text:
                word = word.replace(char, '')
            clean_words.append(word)
    for element in remove_array:
        is_not_thing = lambda x: x is not element
        cleaned_name = list(filter(is_not_thing, clean_words))
    if len(cleaned_name) == 2:
        first_name = cleaned_name[0]
        last_name = cleaned_name[1]
        return {
            'first_name': first_name,
            'last_name': last_name
        }
    else:
        first_name = cleaned_name.pop(0)
        last_name = ''
        for word in cleaned_name:
            last_name += ' ' + word
        return {
            'first_name': first_name.strip(),
            'last_name': last_name.strip()
        }


def clean_up_nav(data):
    """
    Description: removes unwanted results
    or letters from a sales nav crawl
    -------------------------------------
    :param array: an array that has gone
    through LinkedIn crawler methods
    :return clean_array: a clean array
    -------------------------------------
    Use: v = x.clean_up(array)
    """
    clean_data = {
        'contacts': []
    }

    while not data['contacts'] == []:
        new_contact = data['contacts'].pop()

        if new_contact['name'] != 'LinkedIn Member' and '.' not in new_contact['name']:
            name = find_name(new_contact['name'])
            split_info = new_contact['other_info'].strip().splitlines()
            title = split_info[0].split(' at')[0].split('\n')[0]
            company = new_contact['company'].split('\n')[0]
            print(title)

            contact = {
                'first_name': name['first_name'],
                'last_name': name['last_name'],
                'company': company,
                'title': title
            }

            clean_data['contacts'].append(contact)
        
    return clean_data


def linkedin_scrape(url):
    '''
    scrapes a LinkedIn url for all user data
    :param url: url to scrape through
    :return clean_data: returns the cleaned scrape data
    '''
    driver = get_driver(True)

    login(driver)
    time.sleep(5)

    driver.get(url)

    # wait for the result count an calculate pages to look through
    wait_for_element('artdeco-tab-primary-text', driver, "class")
    result_amount = driver.find_element_by_class_name('artdeco-tab-primary-text').text

    pages = page_amount(result_amount)

    data = get_pages_data(pages, driver)
    clean_data = clean_up_nav(data)
    return clean_data


# LINKEDIN ACCOUNT FUNCTIONS

def get_pages_data_accounts(pages, driver):
    '''

    :param pages:
    :param driver:
    :return:
    '''
    data = {
        'contacts': []
    }
    for page in range(pages):
        next_page_class = 'search-results__pagination-next-button'
        wait_for_element(next_page_class, driver, 'class')

        next_page_button = driver.find_element_by_class_name(next_page_class)
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).perform()
        time.sleep(3)

        names = driver.find_elements_by_class_name("result-lockup")
        print('\n\nnames:')
        print(names)
        for element in names:
            try:
                profile_url_element = element.find_element_by_class_name("result-lockup__name")
                profile_url = profile_url_element.find_element_by_css_selector('a').get_attribute('href')
                name = profile_url_element.text
                contact = {
                    'name': name,
                    'profile_url': profile_url
                }
                print(contact)
                data['contacts'].append(contact)
            except Exception as e:
                print(e)
                pass

        try:
            wait_for_element(next_page_class, driver, 'class')

            next_page_button = driver.find_element_by_class_name(next_page_class)
            actions = ActionChains(driver)
            actions.move_to_element(next_page_button).click().perform()
            time.sleep(4)
        except Exception as e:
            print(e)

    return data


def linkedin_account_scrape(url):
    '''
    scrapes a LinkedIn url for all account data
    :param url: url to scrape through
    :return clean_data: returns the cleaned scrape data
    '''
    driver = get_driver(True)

    login(driver)
    time.sleep(5)

    driver.get(url)

    # wait for the result count an calculate pages to look through
    wait_for_element('spotlight-result-count', driver, "class")
    result_amount = driver.find_element_by_class_name('artdeco-tab-primary-text').text
    print('\nResult amount: ')
    print(result_amount)

    pages = page_amount(result_amount)

    data = get_pages_data_accounts(pages, driver)
    return data


def relevant_result(url, company):
    '''
    Checks if url is relevant to the company
    :param url: url to check
    :param company: company to find url for
    :return: bool - if relevant or not
    '''
    false_results = [
        'wikipedia', 'google', 'facebook',
        'linkedin', 'twitter', 'youtube',
        'nytimes', 'yelp', 'crunchbase',
        'newswire', 'yelpblog', 'businessinsider',
        'instagram', 'techcrunch', 'inc.com',
        'wired.com', 'pinterest', 'indeed',
        'glassdoor', 'ratemyemployer', 'bloomberg',
        'tripadvisor', 'booking.com', 'kijiji',
        'yellowpages', 'businesswire'
    ]
    if url is None:
        return False
    for result in false_results:
        if result in url and result not in company:
            return False
    return True


def get_result_links(results):
    '''
    gets links from google result objects
    :param results:
    :return:
    '''
    urls = []
    while not results == []:
        result = results.pop(0)
        url_list = result.find_elements_by_tag_name('a')
        while not url_list == []:
            urls.append(url_list.pop().get_attribute('href'))
    return urls


def parse_domain(unparsed_url):
    '''
    parsed a domain for the base domain
    :param unparsed_url: unparsed domain to fix
    :return: parsed domain
    '''
    if not unparsed_url == '' and unparsed_url is not None:
        new_extract = tldextract.extract(unparsed_url)
        return new_extract.registered_domain
    return None


def fix_url(url):
    if url is None:
        return None
    replace_url = url.replace('mailto:?body=', 'https://www.').replace('%20', ' ').replace('%3A', ':').replace('%2F', '/').replace('#', '')
    return replace_url.split(' ')[0]


def google_company_search(location, company, driver):
    '''
    scrapes google for a company
    :param location: location the search should be in
    :param company: company to search for
    :param driver: currently active chrome driver
    :return:
    '''
    time.sleep(1.5)
    search = company.replace(" ", "+")
    driver.get("https://www.google.ca/search?q={}".format(search + '+' + location))

    wait_for_element("srg", driver, "class")
    results = driver.find_elements_by_class_name("r")
    urls = get_result_links(results)
    parsed_url = None
    possible_result = False

    while not possible_result and not urls == []:
        url = fix_url(urls.pop(0))
        if url is not None:
            parsed_url = parse_domain(url)
            possible_result = relevant_result(parsed_url, company)

    if possible_result:
        print('company: ')
        print('Using: ' + parsed_url)
        return parsed_url
    return None


def google_pages_scrape(search_term, driver, pages=1):
    '''
    scrapes google for a company
    :param search_term: company to search for
    :param pages: number of pages to scrape
    :param driver: currently active chrome driver
    :return:
    '''
    time.sleep(1.5)
    search = search_term.replace(" ", "+")
    driver.get("https://www.google.ca/search?q={}".format(search))
    domains = []

    while pages:
        wait_for_element("srg", driver, "class")
        results = driver.find_elements_by_class_name("r")
        urls = get_result_links(results)

        next_page_button = driver.find_element_by_class_name('pn')
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).perform()

        while not urls == []:
            url = fix_url(urls.pop(0))
            if url is not None:
                parsed_url = parse_domain(url)
                possible_result = relevant_result(parsed_url, search_term)

                if possible_result:
                    print('Accepting: ' + parsed_url)
                    domains.append(parsed_url)

        next_page_button = driver.find_element_by_class_name('pn')
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).click().perform()

        pages -= 1

    return domains


def url_email_scrape(driver, url):
    '''
    Scrapes the email from a webpage
    :param driver: currently active selenium driver
    :param url: url to scrape
    :return email: returns the email if found - else None
    '''
    contact_paths = [
        '', '/contact', '/contact-us'
    ]
    results = None
    found = False
    count = 0
    if 'http' not in url and 'https' not in url:
        url = 'http://' + url
    while not found and count < 3:
        try:
            driver.get(url + contact_paths[count])
            print('Checking ' + url + contact_paths[count])
            time.sleep(5)
            results = driver.find_element_by_xpath("//*[text()[contains(.,'@')]]")
        except Exception:
            print('Error')
            results = None
        if results and results.text:
            found = True
        else:
            print('No email found on ' + url + contact_paths[count])
        count += 1
    if found:
        return results.text
    else:
        return None


def linkedin_nav_headcount_scrape(accounts):
    '''
    Retrieves the employees on LinkedIn company headcount
    :param accounts: accounts to scrape url for headcount
    :return clean_accounts: the number of employees on LinkedIn
    '''
    try:
        driver = get_driver(True)
        print('\n\n------ Logging in to LinkedIn ------\n\n')
        login(driver)
        time.sleep(4)
        clean_accounts = []
        while accounts:
            try:
                account = accounts.pop()
                print('Checking account:')
                print(account)
                url = account[1]
                driver.get(url)
                target_element_name = 'cta-link'
                wait_for_element(target_element_name, driver, "class")
                count = driver.find_element_by_class_name(target_element_name).text
                count_split = count.split(' ')
                count_num = int(count_split[0].replace(',', ''))
                print('\nEmployee count:')
                print(count_num)
                print()
                account.append(count_num)
                print('\nAdding Account\n\n')
                print(account)
                clean_accounts.append(account)
                time.sleep(4)
            except Exception as e:
                print(e)
                print('\n\n----- Error getting account -----\n\n')
                time.sleep(3)
        return clean_accounts
    except Exception as e:
        print(e)
        print('Login Error')
        return []


def quora_question_scraper(url):
    '''

    :param url:
    :return contacts: array of contacts who followed posts on the quora page
    '''
    driver = get_driver(True)
    driver.get(url)
    questions = driver.find_elements_by_class_name('question_link')
    while questions:
        question = questions.pop()
        driver.get(question)
        time.sleep(3)
        follower_button = driver.find_element_by_class_name('')
        actions = ActionChains(driver)
        actions.move_to_element(follower_button).click().perform()
        #ADD SCROLLING TO BOTTOM OF FOLLOWERS


def linkedin_profile_scraper(driver, url):
    '''
    scrapes data off a linkedin profile
    :param driver: currently active driver
    :param url: profile url to scrape from
    :return contact: returns the contact data as an array
    '''
    driver.get(url)
    time.sleep(3)
    profile = []
    name = driver.find_element_by_class_name('pv-top-card-section__name')
    title = driver.find_element_by_class_name()
    return profile


def linkedin_comment_scraper(driver, url):
    '''
    Scrapes leads from a post on LinkedIn
    :param url: url to scrape leads from
    :param driver: currently active driver
    :return contacts: returns the contacts from the post
    '''
    scraped_profiles = []
    try:
        driver.get(url)
        time.sleep(3)
        # PUT IN A WAIT FOR ELEMENT HERE
        button_id = 'show_prev'
        more_comments_button = driver.find_elements_by_id(button_id)

        while more_comments_button:
            actions = ActionChains(driver)
            actions.move_to_element(more_comments_button).click().perform()
            more_comments_button = driver.find_elements_by_id(button_id)

        linkedin_profile_links = driver.find_element_by_class_name('feed-shared-post-meta__profile-link')

        while linkedin_profile_links:
            link = linkedin_profile_links.pop()
            profile_scrape = linkedin_profile_scraper(driver, link)
            if profile_scrape:
                scraped_profiles.append(profile_scrape)
        return scraped_profiles
    except Exception as e:
        print(e)
        return []


def linkedin_post_scraper(urls):
    '''
    scrape multiple posts from LinkedIn
    :param urls: all the post urls to scrape from
    :return contacts: returns contacts from multiple posts
    '''
    contacts = []
    driver = get_driver(True)
    while urls:
        new_contacts = linkedin_comment_scraper(driver, urls.pop())
        time.sleep(3)
        while new_contacts:
            contacts.append(new_contacts.pop())
    return contacts


def linkedin_like_post(url, account):
    '''
    Logs in and likes a post on LinkedIn
    :param url: post url of the post to like
    :param account: account to like from {"username": "example@example.com", "password": "password345"}
    :return:
    '''
    try:
        driver = get_driver(True)
        user_login(driver, account)
        time.sleep(2)
        driver.get(url)
        time.sleep(3)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # WAIT FOR LIKE ELEMENT
        like_button_class = 'like-button'
        element = driver.find_element_by_class_name(like_button_class)
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
    except Exception as e:
        print(e)
        print('Error liking LinkedIn post')


def linkedin_account_domain(nav_results, driver):
    '''
    Scrapes the company domain from the sales nav page
    :param nav_results: array of the account sales nav profile urls
    :param driver: the currently active driver
    :return: array - the company domain from sales nav - removes company if domain not found
    '''
    clean_results = []
    if nav_results is None:
        print('-- ERROR: scrape accounts before using company_domain_scrape() --')
    else:
        while nav_results:
            nav_result = nav_results.pop()
            try:
                driver.get(nav_result['profile_url'])
                time.sleep(1)

                next_page_class = 'search-results__pagination-next-button'
                wait_for_element(next_page_class, driver, 'class')

                next_page_button = driver.find_element_by_class_name(next_page_class)
                actions = ActionChains(driver)
                actions.move_to_element(next_page_button).perform()
                time.sleep(3)

                company_url = 'website'
                element = driver.find_element_by_class_name(company_url)
                nav_result['domain'] = element.find_element_by_css_selector('a').get_attribute('href')

                next_page_button = driver.find_element_by_class_name(next_page_class)
                actions = ActionChains(driver)
                actions.move_to_element(next_page_button).click().perform()
                time.sleep(2)

            except Exception as e:
                print(e)
    return clean_results

