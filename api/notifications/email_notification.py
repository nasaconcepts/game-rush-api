from api.notifications.email_config import email_server, sender_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class email_notifier:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    email_verification_url = os.getenv("VERIFICATION_URL")

    def build_email_body(self, data):
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = data["email"]
            msg["Subject"] = f"Game Update - {data['gameId']}"

            # HTML Content
            html_content = f"""
            <html>
            <body>
                <h2>Hello,</h2>
                <p>Here is an update for Game ID: <b>{data['gameId']}</b></p>
                <p>Stay tuned for more updates!</p>
                <p><a href="{data['gameUrl']}" style="color:blue; font-size:16px;">Join the Game Now</a></p>
                <p>If you have any issues, copy and paste this URL into your browser:</p>
                <p>{data['gameUrl']}</p>
                <br>
                <p>Best Regards,</p>
                <p><b>Your Game Team</b></p>
            </body>
            </html>
            """
            msg.attach(MIMEText(html_content, "html"))

            return msg.as_string()

        except Exception as e:
            print(f"Failed to send email to {data["email"]}: {e}")

        pass

    def send_email_notifications(self, data):
        successful_emails = []
        for recipient_email in data["emails"]:
            try:

                email_data = {"gameId": data["gameId"], "email": recipient_email}
                message = self.build_email_body(email_data)
                # Enable this command when smtp is configured
                email_server.sendmail(sender_email, recipient_email, message)
                email_server.quit()

                successful_emails.append(recipient_email)
            except Exception as ex:
                print(f"Error sending email to {recipient_email}, error->{ex}")
        return successful_emails

    def send_verification_email(self, email, token):
        """Sends a verification email with the token link."""
        try:
            subject = "Verify Your Email"
            verification_link = f"{self.email_verification_url}/api/verify-email/{token}/"
            message = f"Click the link below to verify your email:\n\n{verification_link}"
            # Create a MIME message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "html"))
            print("Email sent successfully!")

            email_server.sendmail(sender_email, email, msg.as_string())
            email_server.quit()

        except Exception as ex:
            print(f"Error sending email to {email}, error->{ex}")
