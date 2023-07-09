from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name:'
        self.fields['email'].widget.attrs['placeholder'] = 'Email:'
        self.fields['text'].widget.attrs['placeholder'] = 'Comment'
        self.fields['text'].widget.attrs['class'] += ' mb-3'

    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')
