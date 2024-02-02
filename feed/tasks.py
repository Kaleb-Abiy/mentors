from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_link(request, user, mentor, link):
    user_email_address = user.email
    mentor_email_address = mentor.email
    from_email = settings.EMAIL_HOST_USER
    subject = "Zoom link for your appointment"
    send_mail(
        subject,
        link,
        from_email,
        [user_email_address, mentor_email_address],
        fail_silently=False,
    )
    print('email sent')