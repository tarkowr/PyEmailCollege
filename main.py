import universities
import smtplib
import ssl
import time
import re
import sys


class Mailsploit:

    last_sent_file = None
    sender_email = ''
    password = ''
    counter = 0
    failed = 0

    # Constructor
    def __init__(self, email, password):
        self.sender_email = email
        self.password = password

    # Start the Mailsploit module
    def run(self):
        start_time = time.time()

        server = self.connect_email()
        last_sent = self.get_last_sent()
        college_list = self.get_colleges()

        self.send_emails(server, college_list, last_sent)

        end_time = round(time.time() - start_time, 1)

        print(f'\nDone! Sent emails to {self.counter} universities in {end_time} seconds')
        self.calc_totals()

        self.last_sent_file.close()

    # Calculates email sending statistics
    def calc_totals(self):
        total = self.counter + self.failed

        if total > 0:
            success_rate = round((self.counter / total) * 100, 1)
            print(f'{success_rate}% success rate')

    # Connect to email server
    def connect_email(self):
        host = 'smtp.gmail.com'
        port = 465

        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(host, port, context=context)
            server.login(self.sender_email, self.password)
        except Exception as err:
            print(f'Unable to connect to G-mail because {err}')
            print('Ensure you entered the correct credentials')
            sys.exit(0)

        return server

    # Read in email message
    @staticmethod
    def get_email_msg():
        body = ''

        with open("email_message.txt", "r") as msg_file:
            for line in msg_file.readlines():
                body += line

        return body

    # Get last email sent
    def get_last_sent(self):
        self.last_sent_file = open("last_sent.txt", "r+")
        last_sent = self.last_sent_file.read()

        print(f'Last sent email: {last_sent}\n')
        return last_sent

    # Overwrite last sent file with latest email attempt
    def write_last_sent(self, domain):
        self.last_sent_file.seek(0)
        self.last_sent_file.write(domain)
        self.last_sent_file.truncate()

    # Return all colleges by country from the API
    @staticmethod
    def get_colleges():
        search_country = 'United States'
        uni = universities.API()

        return uni.search(country=search_country)

    # Clean the domain name from the university API
    @staticmethod
    def clean_domain(domain):
        clean = domain

        # Strip www. from any university domain
        if domain[:4] == 'www.':
            clean = domain[4:]

        return clean

    # Send the email to each college
    def send_emails(self, server, colleges, last_sent):
        found = False
        prefix = 'admissions@'
        subject = 'Subject: Incoming Freshman Information\n'
        body = self.get_email_msg()

        for college in colleges:

            domain = college.domains[0]
            domain = self.clean_domain(domain)

            if domain == last_sent:
                found = True
                continue

            if not found and last_sent is not '':
                continue

            intro = f'Dear {college.name}, \n\n'
            msg = subject + intro + body
            recipient = prefix + domain

            recipient = recipient.encode('ascii', 'ignore').decode('ascii').strip()

            print(f'Sending email to {recipient}')

            self.write_last_sent(domain)

            try:
                # Send email
                server.sendmail(self.sender_email, recipient, msg)

                self.counter += 1
                print('Sent!')

            except Exception as err:
                print(f"Unable to send email to {domain} because {err}")
                self.failed += 1

                err_name = type(err).__name__

                if err_name == 'SMTPSenderRefused':
                    print("G-mail is temporarily disabling you from sending emails. Try again in a couple of minutes!")
                elif err_name == 'SMTPDataError' and re.search('Daily user sending quota exceeded', str(err)) is not None:
                    print("Your daily quota of sending emails has exceeded. Try again tomorrow!")

                if re.search('^\'ascii\' codec can\'t encode character.*$', str(err)) is None:
                    break


mailsploit = Mailsploit('email', 'password')
mailsploit.run()
