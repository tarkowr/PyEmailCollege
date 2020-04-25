# PyEmailCollege

[How to send an email in Python](https://realpython.com/python-send-email/)

### Installation
* Clone this repo from GitHub
 ```bash
 git clone https://github.com/tarkowr/PyEmailCollege.git
 ```
* Enter your email and password into `Mailsploit` at the bottom of the program
```
mailsploit = Mailsploit('email@example.com', 'password')
```
* Go to https://myaccount.google.com/lesssecureapps and make sure the switch is flipped on (toggle it if it isn't)
* Enter your email message into the `email_message.txt` file
* Change the default country (if needed) in the `search_country` variable
```python
search_country = "United States"
```
* Change the default subject header (if needed) in the `subject` variable. Do NOT remove the "Subject: " characters within the subject string!
```python
subject = "Subject: Introduction"
```
* Run the program! If the program fails for whatever reason, start it again, and it will pick back up after the last sent email.
```bash
python main.py
```