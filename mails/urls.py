from django.urls import path
from .views import EmailActivatedView, activate

app_name = 'mails'

urlpatterns = [
    path('email_activated/', EmailActivatedView.as_view(), name='email_activated'),
    path('activate/<uidb64>/', activate, name='activate'),
]
