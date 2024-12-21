from django.template import context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_review_email(name,email,review):
    context={
        'name':name,
        'email':email,
        'review':review
    }
    email_subject='Thank you for visiting and review'
    email_body=render_to_string('email_message.txt',context)

    email=EmailMessage(
        email_subject,email_body,settings.DEFAULT_FROM_EMAIL,[email,'jamesjuliet72@gmail.com'],
    ) 
    return email.send(fail_silently=False)