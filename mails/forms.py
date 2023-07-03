from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control mb-3 mb-lg-0"
        self.fields['name'].widget.attrs['placeholder'] = "Full Name"
        self.fields['name'].widget.attrs['id'] = "colFormLabel"
        self.fields['email'].widget.attrs['placeholder'] = "Email Address"

    class Meta:
        model = Subscriber
        fields = ['name', 'email']
