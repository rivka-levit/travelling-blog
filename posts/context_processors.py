from .models import Category, Author


def category_links(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def blog_author(request):
    author = Author.objects.get(is_owner=True)
    return dict(blog_author=author)
