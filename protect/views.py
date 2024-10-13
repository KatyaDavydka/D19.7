from django.shortcuts import render, redirect

from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_filters import FilterSet

from doska_ob.models import Comment, Post

from protect.models import User


class PostFilter(FilterSet):
    class Meta:
        model = Comment
        fields = [
            'post'
        ]

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(user_id=kwargs['request'])


class IndexView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'protect/index.html'
    context_object_name = 'comments'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset().filter(post__user_id=self.request.user.id)
        self.filterset = PostFilter(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs

        return Comment.objects.none()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Comment.objects.filter(post__user_id=self.request.user.id)
        context['filterset'] = self.filterset
        return context


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'protect/invalid_code.html')
        return redirect('account_login')
