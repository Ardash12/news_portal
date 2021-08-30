from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from .filters import PostFilter, F, C, X  # импортируем недавно написанный фильтр
from .models import Post, BaseRegisterForm, Category
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 5  # поставим постраничный вывод в один элемент
    # form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.all().count()
        context['category'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, *kwargs)


class CategoryDetail(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.filter(postCategory__id=self.kwargs['pk']).count()
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Post.objects.filter(postCategory__id=self.kwargs['pk'])


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-dateCreation')
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


def user_list(request):
    f = F(request.GET, queryset=User.objects.all())
    return render(request, 'user_t.html', {'filter': f})


def post_list(request):
    c = C(request.GET, queryset=Post.objects.all())
    return render(request, 'post_t.html', {'filter': c})


def comment_list(request):
    x = X(request.GET, queryset=Post.objects.all())
    return render(request, 'comment_t.html', {'filter': x})


class PostDetail(DetailView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('articles.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('articles.change_post',)
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('articles.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    autors_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        autors_group.user_set.add(user)
    return redirect('/')


def subscribe(request, pk):
    pass
    # post = Post.objects.get(id=pk)
    # cat_id = post.postCategory.values('id')
    # user = request.user
    # subscriber = User.objects.filter(username=str(user)).last()
    # for i in cat_id:
    #     category = Category.objects.filter(id=i).last()
    #     category.subscribers.add(subscriber)
    # cat = Category.objects.all().values('subscribers')

    # return render(request, 'subscribe.html', {'obj': cat})
    # user = request.user
    # subscriber = User.objects.filter(username=user).last()
    # cat_id = Post.objects.filter(id=pk).values('postCategory__id')
    # category = Category.objects.filter(id=cat_id).last()
    # category.subscribers.add(subscriber)
    # return HttpResponse(f'{subscriber.username}')
    # return HttpResponse(reverse('post_list', args=[str(pk)]))



