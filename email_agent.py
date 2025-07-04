import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

import ssl
import certifi

# Set SSL certificate path to handle certificate issues
os.environ['SSL_CERT_FILE'] = certifi.where()

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body """
    try:
        # Create SSL context with proper certificate verification
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        
        # Get email addresses from environment variables with fallback
        from_email_addr = os.environ.get('FROM_EMAIL', 'your_email@example.com')
        to_email_addr = os.environ.get('TO_EMAIL', 'your_email@example.com')
        
        from_email = Email(from_email_addr)
        to_email = To(to_email_addr)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content).get()
        response = sg.client.mail.send.post(request_body=mail)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)