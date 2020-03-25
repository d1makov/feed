from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView, UpdateView
from django.views import View
# Create your views here.
from .models import Post, Follower
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.models import User


class Home(ListView):
    # Хочу відфільтрувати пости, щоб відображались лише пости юзерів яких фоловить залогінений юзер
    # queryset = Post.objects.exclude(author__users=request.user)
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = '-creation_date'
    paginate_by = 3


class UsersView(TemplateView):
    template_name = 'post/users.html'

    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        follows = Follower.objects.get(current_user=request.user)
        follows = follows.users.all()

        args = {
            'users': users, 'follows': follows
        }
        return render(request, self.template_name, args)


@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    login_url = 'post/login.html'

    def get(self, request, *args, **kwargs):
        view = Home.as_view(
            template_name = 'post/admin_page.html',
            paginate_by = 4
        )
        return view(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post

    def get_object(self):
        object = super(PostDetail, self).get_object()
        # object.read = True
        # object.save()
        return object


class PostCreate(CreateView):
    model = Post
    fields = ('title', 'body')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(PostCreate, self).form_valid(form)


# @login_required(login_url='/accounts/login/')
class FeedView(UpdateView):
    template_name = 'post/feed.html'

    def get(self, request, *args, **kwargs):
        follows = Follower.objects.get(current_user=request.user)
        follows = follows.users.all()
        posts = Post.objects.all().filter(author__in=follows).order_by('-creation_date')
        args = {
            'posts': posts, 'follows': follows
        }
        return render(request, self.template_name, args)


class MarkAsReadView(UpdateView):
    model = Post
    fields = ['read']
    template_name = 'post/feed.html'

