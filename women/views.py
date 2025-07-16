from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles

import uuid

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


# def index(request):
#     posts = Women.published.all().select_related('cat')
#
#     data = {
#         'title': "Главная страница",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#
#     return render(request, template_name='women/index.html', context=data)


class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': "Главная страница",
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # posts = Women.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def handle_uploaded_file(f):
#     with open(f'uploads/{uuid.uuid4().hex[0:8]}.{f.image.format.lower()}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, template_name='women/about.html', context={
        'title': "О сайте", 'menu': menu, 'form': form}, )


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # # print(form.cleaned_data)
#             # title = form.cleaned_data['title']
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}
#     return render(request, 'women/addpage.html', context=data)


# В учебных целях
class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}
        return render(request, 'women/addpage.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}
        return render(request, 'women/addpage.html', context=data)


def contact(request):
    return HttpResponse("Контакты для связи")


def login(request):
    return HttpResponse("Страница авторизации")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    # Используем 2 независимых запроса, чтобы не отрабатывалось дважды
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")

    data = {
        'title': f"Рубрика: {category.name}",
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, template_name='women/index.html', context=data)


class WomenCategory(ListView):
    model = Category
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = f"Категория - {cat.name}"
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'{tag.tag}',
#         "menu": menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)


class WomenTagPostList(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, cat=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['tag_slug']
        tag = TagPost.objects.get(slug=slug).tag
        context['title'] = f"Тег - {tag}"
        context['menu'] = menu
        context['cat_selected'] = None
        return context
