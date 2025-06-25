from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

# Create your views here.
from django.urls import reverse

from women.forms import AddPostForm
from women.models import Women, Category, TagPost

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


def index(request):
    posts = Women.published.all().select_related('cat')

    data = {
        'title': "Главная страница",
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }

    return render(request, template_name='women/index.html', context=data)


def about(request):
    return render(request, template_name='women/about.html', context={
        'title': "О сайте", 'menu': menu}, )


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            title = form.cleaned_data['title']
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()

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


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'{tag.tag}',
        "menu": menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)
