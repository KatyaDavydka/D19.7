from django.conf import settings
from django.shortcuts import render, redirect

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)

from .filters import PostFilter
from .models import *

from .forms import PostForm, CommentForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.shortcuts import get_object_or_404

import pytz
from django.utils import timezone

from django.core.mail import send_mail


class PostList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 7

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        return context


class PostCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def post(self, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = self.request.user
            comment.save()
            send_mail(
                subject=f'New Comment on"{comment.post.header}"',
                message=f'Был оставлен отклик {comment.comm_text} пользователем {self.request.user.username} на ваше объявление "{comment.post.header}"',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[comment.post.user.email]
            )
            return redirect('post_detail', pk=post.pk)

    def get_object(self, *args, **kwargs):
        from django.core.cache import cache
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get
        # действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'post_search.html'
    context_object_name = 'post'
    paginate_by = 2


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filterset'] = self.filterset
    return context


class PostUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post')


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('post.add_post',)


class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('post.change_post',)


def accept(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.status == 'pending':
        comment.status = 'accepted'
        comment.save()
        send_mail(
            subject=f'Оповещение',
            message=f'Ваш отклик "{comment}" был принят автором {comment.post.user.username}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[comment.user.email],
        )
    return redirect('profile')
