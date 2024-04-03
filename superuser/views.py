from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from config.settings import EMAIL_HOST_USER


def send_email(request):
    if request.method == 'POST':
        try:
            recipient_list = [user.email for user in User.objects.all()]

            send_mail(
                subject=request.POST['subject'],
                message=request.POST['message'],
                from_email=EMAIL_HOST_USER,
                recipient_list=recipient_list
            )
            return HttpResponse('<h1>Email sent!</h1>')
        except Exception as e:
            return HttpResponse(f'<h1>Something went wrong</h1><p>{e}</p>', status=500)
    return render(request, 'superuser/email_message.html')
