from django.shortcuts import render
from django.views.generic import ListView, View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post


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

        return render(request, 'posts/home.html', {
            'latest_posts': Post.objects.all().order_by('-created_at')[:3],
            'posts': page_obj
        })


class PostDetailView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, 'posts/post_detail.html', {
            'post': post
        })
