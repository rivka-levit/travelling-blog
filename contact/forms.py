from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.fields['sender_name'].widget.attrs['class'] = 'form-control form-control-name'
        self.fields['sender_name'].widget.attrs['id'] = 'sender_name'
        self.fields['sender_email'].widget.attrs['class'] = 'form-control form-control-email'
        self.fields['sender_email'].widget.attrs['id'] = 'sender_email'
        self.fields['text'].widget.attrs['class'] = 'form-control form-control-message'
        self.fields['text'].widget.attrs['id'] = 'message'

    class Meta:
        model = ContactMessage
        fields = ('sender_name', 'sender_email', 'text')
