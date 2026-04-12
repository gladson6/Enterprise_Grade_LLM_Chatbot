import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
from app.models.schemas import Lead

class EmailService:
    """
    A service to handle sending emails, for example, for lead notifications.
    """
    def __init__(self):
        self.config = settings
        self.is_configured = all([
            self.config.SMTP_SERVER,
            self.config.SMTP_PORT,
            self.config.SMTP_USERNAME,
            self.config.SMTP_PASSWORD,
            self.config.EMAIL_SENDER_ADDRESS,
            self.config.EMAIL_RECIPIENT_ADDRESS,
        ])
        if not self.is_configured:
            print("WARN: Email service is not configured. Leads will be printed to console only.")

    def send_lead_notification(self, lead: Lead):
        """Sends an email notification with the new lead details."""
        if not self.is_configured:
            return

        subject = f"New Chatbot Lead: {lead.name}"
        body = f"""
        A new lead has been captured by the website chatbot.

        Details:
        - Name: {lead.name}
        - Email: {lead.email}
        - Company: {lead.company or 'Not provided'}
        - Original Query: {lead.query}

        Please follow up promptly.
        """

        msg = MIMEMultipart()
        msg['From'] = self.config.EMAIL_SENDER_ADDRESS
        msg['To'] = self.config.EMAIL_RECIPIENT_ADDRESS
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            print(f"Sending lead notification email to {self.config.EMAIL_RECIPIENT_ADDRESS}...")
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as server:
                server.starttls()
                server.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
                server.send_message(msg)
            print("Email sent successfully.")
        except Exception as e:
            print(f"ERROR: Failed to send email. Error: {e}")

# Singleton instance
email_service = EmailService()
