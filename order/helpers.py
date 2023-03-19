from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_mail(user_obj,email,token):
    subject='Your forgot password link'
    message=f'Hi {user_obj},click on the link to reset your password http://127.0.0.1:8000/confirm_pwd{token}'
    email_from=settings.EMAIL_HOST_USER
    receipient_list=[email]
    send_mail(subject,message,email_from,receipient_list)
    return True