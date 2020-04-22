import universities
import smtplib
import ssl
import time
import re
import sys

msg_file = open("email_message.txt", "r")
last_sent_file = open("last_sent.txt", "r+")

# Program vars
counter = 0
failed = 0
search_country = 'United States'
start = False
last_sent = None
uni = universities.API()
start_time = time.time()

# Email connection vars
port = 465
sender_email = 'exmaple@domain.com'
password = 'password'

# Email message vars
prefix = 'admissions@'
subject = 'Subject: Incoming Freshman Information\n'
body = ''

# Connect to email client
try:
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
    server.login(sender_email, password)
except Exception as err:
    print(f'Unable to connect to G-mail because {err}')
    print('Ensure you entered the correct credentials')
    sys.exit(0)

# Read in email message
for line in msg_file.readlines():
    body += line

# Get last email sent
last_sent = last_sent_file.read()

print(f'Last sent email: {last_sent}\n')

colleges = uni.search(country=search_country)

for college in colleges:

    domain = college.domains[0]

    # Strip www. from any university domain
    if domain[:4] == 'www.':
        domain = domain[4:]

    # Start emailing after the last university email attempt
    if domain == last_sent:
        start = True
        continue

    if start:
        try:
            intro = f'Dear {college.name}, \n\n'
            msg = subject + intro + body
            recipient = prefix + domain

            recipient = recipient.encode('ascii', 'ignore').decode('ascii').strip()

            print(f'Sending email to {recipient}')

            # Overwrite last sent file with latest email attempt
            last_sent_file.seek(0)
            last_sent_file.write(domain)
            last_sent_file.truncate()

            # Send email
            server.sendmail(sender_email, recipient, msg)

            counter += 1
            print('Sent!')

        except Exception as err:
            print(f"Unable to send email to {domain} because {err}")
            failed += 1

            err_name = type(err).__name__

            if err_name == 'SMTPSenderRefused':
                print("G-mail is temporarily disabling you from sending emails. Try again in a couple of minutes!")
            elif err_name == 'SMTPDataError' and re.search('Daily user sending quota exceeded', str(err)) is not None:
                print("Your daily quota of sending emails has exceeded. Try again tomorrow!")

            if re.search('^\'ascii\' codec can\'t encode character.*$', str(err)) is None:
                break

end_time = round(time.time() - start_time, 1)

print(f'\nDone! Sent emails to {counter} universities in {end_time} seconds')

total = counter + failed

if total > 0:
    success_rate = round((counter/total)*100, 1)
    print(f'{success_rate}% success rate')

msg_file.close()
last_sent_file.close()
