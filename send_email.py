'''
Function for emailing from Python IDE
'''

import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '


def main(to_contacts, subject, attachment_path):
    sender = 'email-slending-from'
    gmail_password = 'email-password'
    recipients = to_contacts

    # Create the enclosing (outer) message
    outer = MIMEMultipart('alternative')
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    html = """\
    email body html
    """

    # Record the MIME types of both parts - text/plain and text/html.
    text = 'hi'
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    outer.attach(part1)
    outer.attach(part2)

    # List of attachments
    attachments = attachment_path

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()
