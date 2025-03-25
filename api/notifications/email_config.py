import smtplib
import os


smtp_server = os.getenv("SMTP_SERVER") # Change for your provider
smtp_port = int(os.getenv("SMTP_PORT"))
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")  # Use App Password for Gmail
email_server = smtplib.SMTP(smtp_server, smtp_port)
email_server.starttls()