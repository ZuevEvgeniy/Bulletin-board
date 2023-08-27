from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from datetime import datetime
from .models import Post, Comment
from .filters import ComsFilter
from .forms import PostForm, ComForm
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail

class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

@method_decorator(login_required, name='dispatch')
class PostCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('announcement.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs

@method_decorator(login_required, name='dispatch')
class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('announcement.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs

@method_decorator(login_required, name='dispatch')
class PostDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('announcement.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

@method_decorator(login_required, name='dispatch')
class ComCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('announcement.add_comment',)
    form_class = ComForm
    model = Post
    template_name = 'com_edit.html'

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs

    def form_valid(self, form):
        com = form.save(commit=False)
        com.save()
        send_mail(
            subject=f'На Ваш пост{com.post} откликнулся{com.user}',
            message=com.comment_text,
            from_email='ForMyLittleTesting@yandex.ru',
            recipient_list=["authors_email"]
        )

        return super().form_valid(form)

class ComDetail(DetailView):
    model = Post
    template_name = 'com.html'
    context_object_name = 'com'
    queryset = Comment.objects.all()

@method_decorator(login_required, name='dispatch')
class ComUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('announcement.change_comment',)
    form_class = ComForm
    model = Comment
    template_name = 'com_edit.html'

    def get_form_kwargs(self):
        """Необходимо учитывать, что текущий пользователь у нас может быть не залогинен."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user_info': self.request.user if self.request.user.is_authenticated else None,
        })
        return kwargs

@method_decorator(login_required, name='dispatch')
class ComDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('announcement.delete_comment',)
    model = Comment
    template_name = 'com_delete.html'
    success_url = reverse_lazy('posts_list')

class ComsSearch(ListView):
    model = Comment
    ordering = '-time_in'
    template_name = 'coms.html'
    context_object_name = 'coms'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ComsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context
