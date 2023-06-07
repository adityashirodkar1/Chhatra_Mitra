import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'chhatramitraspit@gmail.com'
email_password = 'pohfaofishoqguio'
email_body = 'Reminder to complete your assignment'

def send_mail(email_receiver,email_body):
    # Set the subject and body of the email
    subject = 'Reminder To Complete The Assignment!'
    body = email_body

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

#send_mail('csmadityashirodkar@gmail.com',email_body)