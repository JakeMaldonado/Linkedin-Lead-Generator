from main import GenerateKindling, GenerateAccounts, LinkedInPod
from send_email import main
import csv

urls = [
    ['LinkedIn sales nav url', 'location']
]

title = input('Enter title being searched: ')


while not urls == []:

    search = urls.pop()
    url = search[0]
    city = search[1]

    city = city.replace('/', '&')
    title = title.replace('/', '&')

    g = GenerateKindling(url, city)
    c = g.scrape()
    # print(c)
    # print(len(c['contacts']))
    # print()

    completed_leads = g.find_contact_domains(c)

    # print(l)
    # print(len(l['contacts']))
    # print()

    # FIND LEAD TECHNOLOGY
    # completed_leads = g.note_tech(l)
    #
    # completed_leads = g.find_emails(t)
    print(completed_leads)

    l_len = len(completed_leads['contacts'])
    file_name = city.replace(' ', '_') + '_' + title.replace(' ', '_') + '_' + 'output' + '.csv'

    toCSV = completed_leads['contacts']
    if len(toCSV) > 0:
        keys = toCSV[0].keys()

        for lead in completed_leads['contacts']:
            lead['city'] = city

        with open(file_name, "w") as f:
            w = csv.DictWriter(f, keys)
            w.writeheader()
            w.writerows(toCSV)

        name = 'Jake'

        to = ['email/emails to send results to']
        subject = "Hey %s, meet %s's %s %s's" % (name, city, l_len, title)

        attachment_path = [file_name]
        main(to, subject, attachment_path)
