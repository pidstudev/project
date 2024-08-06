from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email_notification(email, subject, body):
    """
    Sends an email notification to the specified email address.
    """
    message = Message(subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
    message.body = body

    try:
        mail.send(message)
        current_app.logger.info(f"Email sent to {email} with subject '{subject}'.")
    except Exception as e:
        current_app.logger.error(f"An error occurred while sending email notification: {str(e)}")

def send_rental_notification(email, rental_details):
    """
    Sends a notification email about a scheduled rental.
    """
    subject = 'Upcoming Rental Reminder'
    body = f"""
    Hello,

    This is a reminder about your upcoming rental:

    Rental Details:
    {rental_details}

    Best regards,
    LakbayPinas
    """
    send_email_notification(email, subject, body)
