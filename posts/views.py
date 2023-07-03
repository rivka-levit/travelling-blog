from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from mails.models import Subscriber
from mails.forms import SubscriberForm


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')[3:]
        page = request.GET.get("page", 1)
        per_page = 3
        orphans = 1
        paginator = Paginator(posts, per_page, orphans)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        form = SubscriberForm()

        return render(request, 'posts/home.html', {
            'latest_posts': Post.objects.all().order_by('-created_at')[:3],
            'posts': page_obj,
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            new_subscriber = Subscriber(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email']
            )
            new_subscriber.save()
        return redirect(request.META['HTTP_REFERER'])


class PostDetailView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, 'posts/post_detail.html', {
            'post': post
        })
