from django.shortcuts import render
from django.views.generic import ListView, View
from .models import Post, Category, Author


class Home(ListView):
    template_name = 'posts/home.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.all().order_by('-created_at')[:3]
        context['posts'] = Post.objects.all().order_by('-created_at')[3:]
        context['blog_author'] = Author.objects.get(pk=1)
        return context


class PostDetailView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, 'posts/post_detail.html', {
            'post': post
        })
