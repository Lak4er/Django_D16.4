from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponse
from django.views import View
# from .tasks import
from datetime import datetime, timedelta


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta=datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/news_lk')

class PostList(ListView):
      model = Post
      ordering = '-time_in_post'
      template_name = 'news.html'
      context_object_name = 'post'
      paginate_by = 5


      def get_queryset(self):
          queryset = super().get_queryset()
          self.filterset = PostFilter(self.request.GET, queryset)
          return self.filterset.qs

      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['filterset'] = self.filterset
          return context

      def get_object(self, *args, **kwargs):
          obj = cache.get(f'post-{self.kwargs["pk"]}',None)
          if not obj:
              obj = super().get_object(queryset=self.queryset)
              cache.set(f'post-{self.kwargs["pk"]}', obj)

          return obj


class PostList_lk(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in_post'
    template_name = 'news_lk.html'
    context_object_name = 'post'
    paginate_by = 5

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class Subscribe(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'subscribe.html'
    context_object_name = 'subscribe'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        usercategory = Subscribers(
            user=self.request.user,
            category_subscribers=self.get_object()
        )
        # try:
        usercategory.save()
        # messages.success(request, f'Вы успешно подписались на раздел {self.get_object().name}')
        # except:
        #     messages.error(request, f'Вы уже подписаны на раздел {self.object().name}')
        return redirect(f'/news/category/{self.get_object().id}/success')



class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post'

class SearchPosts(ListView):
    paginate_by = 10
    model = Post
    ordering = 'time_in_post'
    template_name = 'search.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post',)

class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавить статью"
        return context


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактировать статью"
        return context


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = ('news.delete_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

class Success(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'success.html'
    context_object_name = 'success'


class ClassCategory(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'



