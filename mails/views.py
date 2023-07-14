from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import Subscriber
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def activate(request, uidb64):
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        subscriber = Subscriber.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Subscriber.DoesNotExist):
        subscriber = None

    if subscriber:
        subscriber.is_active = True
        subscriber.save()
        return redirect('mails:email_activated')
    return redirect('home')


class EmailActivatedView(TemplateView):
    template_name = 'mails/email_activated.html'
