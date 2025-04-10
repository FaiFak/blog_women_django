from django import template
import women.views as views
from women.models import Category, TagPost

register = template.Library()


# @register.simple_tag(name='get_cats')
# def get_categories():
#     return views.cats_db

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}
