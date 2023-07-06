from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactMessageForm
from .models import ContactMessage


class ContactView(View):
    def get(self, request):
        form = ContactMessageForm()
        return render(request, 'contact/contact.html', {
            'form': form
        })

    def post(self, request):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            new_message = ContactMessage(
                sender_name=form.cleaned_data['sender_name'],
                sender_email=form.cleaned_data['sender_email'],
                text=form.cleaned_data['text']
            )
            new_message.save()
            return redirect('home')
        return redirect(request.META['HTTP_REFERER'])
