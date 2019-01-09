# Linkedin-Lead-Generator

create a credentials.py file and fill in your info:

```python
HUBSPOT_API_KEY = ''
HUNTER_API_KEY = ''
KINDLING_API_KEY = ''
LINKEDIN_USERNAME = 'YOUR EMAIL'
LINKEDIN_PASSWORD = 'YOUR PASSWORD'

POD_ACCOUNTS = {
"accounts": []
}
```
The only required credentials are LINKEDIN_USERNAME and LINKEDIN_PASSWORD.
Leave the other ones blank even if you don't need them.

Check the tests.py file for an example to run.

You will also need:
 - Selenium, 
 - dnspython and tldextract via pip3,
 - Latest chromedriver from your package manager 
 
 
Note: you may need to add a PATH variable to your bash profile to set the default path to the chromedriver
