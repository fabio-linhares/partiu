import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(smtp_password, from_email, to_email, subject, html_content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        with smtplib.SMTP("smtp.sendgrid.net", 465) as server:
            server.starttls()
            server.login("apikey", smtp_password)
            server.sendmail(from_email, to_email, message.as_string())
        return {"status": "success", "message": "Email enviado com sucesso!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

