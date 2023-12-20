import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHandler:
    @staticmethod
    def send_verification_email(email, message_sender):
        # For demonstration, send a simple verification email
        subject = "FitHub Registration Verification"
        body = "Thank you for registering with FitHub! Your account is now being verified."
        sender_email = "your_sender_email@gmail.com"  # Update with your sender email
        sender_password = "your_sender_password"  # Update with your sender email password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
