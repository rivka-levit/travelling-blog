from django.urls import path
from .views import PostDetailView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post_detail/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
]
