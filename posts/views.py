from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class Home(TemplateView):
    template_name = 'posts/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['title'] = 'Travelling blog - Home'
        return context
