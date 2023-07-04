from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Post, Category
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


class CategoryView(ListView):
    model = Post
    template_name = 'posts/category.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        return super().get_queryset().filter(category=category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        context['category'] = category
        return context


class SearchResultsView(ListView):
    model = Post
    template_name = 'posts/search-results.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        posts = super(SearchResultsView, self).get_queryset()
        query = self.request.GET.get('q')
        if not query:
            return None
        return posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(text__icontains=query)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
