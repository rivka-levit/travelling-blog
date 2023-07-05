from django.shortcuts import render
from django.views.generic import View


class ContactView(View):
    def get(self, request):
        return render(request, 'contact/contact.html')
