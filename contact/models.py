from django.db import models


class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=50)
    sender_email = models.EmailField()
    text = models.TextField(max_length=500, blank=True)
    processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contact message'
        verbose_name_plural = 'Contact messages'

    def __str__(self):
        return f'{self.sender_name} ({self.sender_email})'
