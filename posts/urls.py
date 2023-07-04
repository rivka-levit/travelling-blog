from django.urls import path
from .views import PostDetailView, HomeView, CategoryView, SearchResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post_detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('search-results/', SearchResultsView.as_view(), name='search_results'),
]
