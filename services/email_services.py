import smtplib
from email.mime.text import MIMEText

def send_email(sender, password, receiver, message):
    msg = MIMEText(message)
    msg["Subject"] = "InsightForge Report"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
