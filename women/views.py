from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

# Create your views here.
from django.urls import reverse

from women.models import Women

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Анджелина Джоли (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН. Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'},
]


def index(request):
    posts = Women.published.all()

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
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Контакты для связи")


def login(request):
    return HttpResponse("Страница авторизации")


def show_category(request, cat_id):
    data = {
        'title': "Главная страница",
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }

    return render(request, template_name='women/index.html', context=data)

# def page_not_found(request, exception):
#     return HttpResponseNotFound('<h1>Страница не найдена</h1>')
