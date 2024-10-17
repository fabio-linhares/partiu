from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_email(smtp_password_, from_email_, to_email_, subject_, html_content_):

    message = Mail(
    from_email = from_email_,
    to_emails = to_email_,
    subject = subject_,
    html_content = html_content_)

    try:
        sg = smtp_password_
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)