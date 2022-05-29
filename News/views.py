from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Author, Category, PostCategory
from .models import Post as PostModel
from .filters import NewsFilter
from .forms import PostForm
from .tasks import send_new_mail


class PostList(ListView):
    model = PostModel
    ordering = ['-datetime']
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    template_name = 'post_detail.html'
    queryset = PostModel.objects.all()


class SearchList(ListView):
    model = PostModel
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-datetime']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'create_post.html'
    permission_required = ('news.add_Post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'create_post.html'
    form_class = PostForm
    permission_required = ('news.change_Post')


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return PostModel.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostDelete(DeleteView):
    template_name = 'delete_post.html'
    queryset = PostModel.objects.all()
    success_url = '/news/'
    

class CategorySubscribe(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    email = user.email
    category.subscribers.add(user)
    send_mail(
        subject = f'{category}',
        message = f'Уважаемый "{request.user}"! Вы подписались на обновление категории "{category.article_text}".',
        from_email = 'testskillfactory@gmail.com',
        recipient_list=[email, ],
    )
    
    return redirect('/news')

@login_required
def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    category.subscribers.remove(user)

    return redirect('/news')


def send_mail(instance):
    sub_text = instance.main_part

    for category in instance.postCategories.all():
        for subscriber in category.subscribers.all():
            html_content = render_to_string(
                'mail.html', {'post': instance, 'text': sub_text[:50], 'category': category.article_text})

            username = subscriber.username
            email = subscriber.email

            send_new_mail.delay(username, email, html_content)

        return redirect('/news/')