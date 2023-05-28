from random import randint
from email.message import EmailMessage
import smtplib


# 6 digit number random generate
def gen_otp() -> str:
    """
    Generates a six character string representation of an integer
    :return: random 6 digit string

    Speed tests indicate there is a much faster way of achieving the same result

    New implementation:
        str(randint(100000, 999999))
    389 ns ± 1.76 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)

    Old implementation:
        val = ""
        for i in range(0, 6):
            ran = random.randrange(0, 10)
            val += str(ran)
    2.59 µs ± 9.19 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
    """
    return str(randint(100000, 999999))


# mail  sender option
def sender(to_mail: str, subject: str, messages: str):
    """
    A function that sends an email containing a subject and a message
    :param to_mail:
    :param subject:
    :param messages:
    :return:
    """
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    # Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted
    server.starttls()
    # Log in on an SMTP server that requires authentication. The arguments are the username and the password to authenticate with.
    server.login("hostemail", "enter_your_apikey")
    emails = EmailMessage()
    emails["From"] = "hostemail"
    emails["To"] = to_mail
    emails["Subject"] = subject
    emails.set_content(messages)
    server.send_message(emails)
