from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def count_posts(self):
        return self.posts.count()


class Author(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='author_photos', null=True, blank=True)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, related_name='posts')
    excerpt = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='post_photos')
    time_read = models.IntegerField(blank=True, null=True)
    text = models.TextField(max_length=5000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
