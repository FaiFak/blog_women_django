from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles

import uuid

from women.utils import DataMixin, menu


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    title_page = 'Главная страница'
    cat_selected = 0

    # extra_context = {
    #     'title': "Главная страница",
    #     'menu': menu,
    #     'cat_selected': 0,
    # }

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


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

    title_page = 'Изменение статьи'


class DeletePage(DataMixin, DeleteView):
    model = Women
    success_url = reverse_lazy('home')
    template_name = 'women/delete_page.html'
    title_page = 'Удаление статьи'


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


class WomenCategory(DataMixin, ListView):
    model = Category
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title=f'Категория - {cat.name}',
                                      cat_selected=cat.pk,
                                      )


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


class WomenTagPostList(DataMixin, ListView):
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
        return self.get_mixin_context(context,
                                      title=f'Тег - {tag}',
                                      )
