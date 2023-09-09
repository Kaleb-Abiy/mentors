from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.conf import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_email_verfication(request, user):
    token = PasswordResetTokenGenerator()
    confirmation_token = token.make_token(user)
    email_address = user.email
    from_email = settings.EMAIL_HOST_USER
    domain = request.META['HTTP_HOST']

    activation_link = f'{domain}/auth/verify_email?user_id={user.id}&token={confirmation_token}'

    subject = "email verfication"

    send_mail(
        subject,
        activation_link,
        from_email,
        [email_address,],
        fail_silently=False,
    )

    print('email sent')


def check_confirmation_token(user, token):
    t = PasswordResetTokenGenerator()
    result = t.check_token(user, token)
    return result
