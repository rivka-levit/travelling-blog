from django.shortcuts import render
from django.views.generic import View
from .forms import ContactMessageForm


class ContactView(View):
    def get(self, request):
        form = ContactMessageForm()
        return render(request, 'contact/contact.html', {
            'form': form
        })
