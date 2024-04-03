from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Category, News

from .forms import RegistrationForm


def index(request):
    news = News.objects.all()
    return render(request, 'index.html', {'news': news})


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class CategoriesView(ListView):
    model = Category
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breaking_news'] = Category.objects.get(name='Breaking News')
        context['sport_news'] = Category.objects.get(name='Sport News')
        context['uzbekistan'] = Category.objects.get(name='Uzbekistan')
        context['world_news'] = Category.objects.get(name='World News')
        return context


class NewsAddView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news-or-post/add_news.html'
    fields = ['news_title', 'news_content', 'news_image', 'news_description', 'news_category']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class NewsListView(ListView):
    model = News
    template_name = 'news-or-post/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        if 'category' in self.request.GET:
            try:
                return News.objects.filter(news_category=self.request.GET['category'])
            except:
                return redirect('news_list')
        if 'keyword' in self.request.GET:
            try:
                return (News.objects.filter(
                    news_title__icontains=self.request.GET['keyword']) |
                        News.objects.filter(news_description__icontains=self.request.GET['keyword']) |
                        News.objects.filter(news_content__icontains=self.request.GET['keyword']))
            except:
                return News.objects.none()
        return News.objects.all()


class NewsDetailView(DetailView):
    model = News
    template_name = 'news-or-post/about_news.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        News.objects.filter(pk=self.object.pk).update(news_views_count=F('news_views_count') + 0.5)
        return response


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'news-or-post/edit_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']
    success_url = reverse_lazy('list_news')

    def test_func(self):
        news = News.objects.get(pk=self.kwargs['pk'])
        return self.request.user == news.news_author

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('list_news')
    template_name = 'news-or-post/confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(news_author=self.request.user)
