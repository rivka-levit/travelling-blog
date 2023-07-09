from django.shortcuts import render, redirect
from django.views.generic import ListView, View, TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Post, Category, Comment, Tag
from .forms import CommentForm
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
        try:
            next_post = Post.objects.filter(created_at__gt=post.created_at).\
                order_by('created_at')[0]
        except IndexError:
            next_post = None
        try:
            prev_post = Post.objects.filter(created_at__lt=post.created_at).\
                order_by('-created_at')[0]
        except IndexError:
            prev_post = None

        # Additional posts for the section 'You may also like'
        related_posts = Post.objects.filter(tags__in=post.tags.all()).\
            exclude(pk=post.id).distinct().order_by('-created_at')
        if len(related_posts) > 3:
            related_posts = related_posts[:3]
        else:
            add_posts = Post.objects.filter(category=post.category).\
                exclude(pk=post.id, id__in=related_posts.values_list('id', flat=True)).\
                order_by('-created_at')[:3-len(related_posts)]
            related_posts = list(related_posts)
            related_posts.extend(add_posts)

        # Comment form
        form = CommentForm()

        comments = post.comments.filter(is_moderated=True)

        return render(request, 'posts/post_detail.html', {
            'post': post,
            'next_post': next_post,
            'prev_post': prev_post,
            'related_posts': related_posts,
            'form': form,
            'comments': comments
        })

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if form.is_valid():
            new_comment = Comment(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                text=form.cleaned_data['text'],
                post=post
            )
            new_comment.save()

        return redirect(request.META['HTTP_REFERER'])


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


class AboutView(TemplateView):
    template_name = 'posts/about.html'


class TagSearchView(ListView):
    model = Post
    template_name = 'posts/tag-search.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6
    paginate_orphans = 1

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        tag = Tag.objects.get(name=tag_name)
        return super(TagSearchView, self).get_queryset().filter(tags=tag)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagSearchView, self).get_context_data(**kwargs)
        tag = self.kwargs['tag']
        context['tag'] = tag
        return context
