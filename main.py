import universities
import smtplib
import ssl
import time

msg_file = open("email_message.txt", "r")
last_sent_file = open("last_sent.txt", "r+")

# Program vars
counter = 0
search_country = 'United States'
start = False
last_sent = None
uni = universities.API()
start_time = time.time()

# Email connection vars
port = 465
sender_email = 'example@domain.com'
password = 'password'

# Email message vars
prefix = 'admissions@'
subject = 'Subject: Incoming Freshman Information\n'
body = ''

# Connect to email client
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login(sender_email, password)

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

            print(f'Sending email to {recipient}')

            # Overwrite last sent file with latest email attempt
            last_sent_file.seek(0)
            last_sent_file.write(domain)
            last_sent_file.truncate()

            # Send email
            server.sendmail(sender_email, recipient, msg)

        except Exception as err:
            print(err)
            break

        counter += 1
        print('Sent!')

end_time = round(time.time() - start_time, 1)

print(f'\nDone! Sent emails to {counter} universities in {end_time} seconds')

msg_file.close()
last_sent_file.close()
