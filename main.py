import universities
import smtplib
import ssl

msg_file = open("email_message.txt", "r")
last_sent_file = open("last_sent.txt", "r+")

counter = 0
search_country = 'United States'
start = False
last_sent = ''
uni = universities.API()
port = 465
sender_email = '<replace with email>'
password = '<replace with password>'
prefix = 'admissions@'
body = ''
subject = 'Subject: Incoming Freshman Information\n'

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
            context = ssl.create_default_context()
    
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient, msg)

        except Exception as err:
            print(err)
            break

        counter += 1
        print('Sent!')

print(f'\nDone! Sent emails to {counter} universities in the {search_country}')

msg_file.close()
last_sent_file.close()
