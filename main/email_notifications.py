from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email_notification(email, subject, body):
    """
    Sends an email notification to the specified email address
    """

    message = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    message.body = body

    try:
        mail.send(message)
    except Exception as e:
        print(f"An error occured while sending email notification: {str(e)}")

