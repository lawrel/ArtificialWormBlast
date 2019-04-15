import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid


def send_email(r_email, subjectline, body):
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # get emails to and from
        s_email = "artificialwormblast@gmail.com"
        
        # Log into our account to send email
        server.login("artificialwormblast@gmail.com", "TSITMonsterCards")

        # create message
        message = MIMEMultipart()
        message["From"] = s_email
        message["To"] = r_email
        message["Subject"] = subjectline
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()

        # send message
        server.sendmail(s_email, r_email, text)

def email_reset(email, link):
    body = """
    Hi there!

    It looks like you forgot your password. Sad.

    Well here is a link to reset your password: """ + link + """

    Better luck in remembering your password next time!

    -AWB team
    """
    send_email(email, "Monster's Ink Password Reset", body)


def email_gamelink(email, link):
    body = """
    Hi there!

    It looks like you have a friend. Congratulations!

    Your friend would like to play a game of Monster's Ink with you. Click the link to join them or do not and let them be sad: """ + link + """

    Enjoy your Game!

    -AWB team
    """
    send_email(email, "Monster's Ink Game Invitation", body)
