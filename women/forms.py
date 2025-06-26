from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, TagPost


# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789- "
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел.'
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название статьи',
                            widget=forms.TextInput(attrs={'class': "form-input"}),
                            min_length=5,
                            # validators=[
                            #     RussianValidator()
                            # ],
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка никак'
                            })
    slug = forms.SlugField(max_length=255, label='URL', )
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, label='Статус', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж',
                                     empty_label='Не замужем')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError(message='Должны присутствовать только русские символы, дефис и пробел.')

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')
        content = cleaned_data.get('content')
        is_published = cleaned_data.get('is_published')
        cat = cleaned_data.get('cat')
        husband = cleaned_data.get('husband')

        if not title and not slug:
            msg = 'Укажите имя и slug записи'
            self.add_error(title, msg)
            self.add_error(slug, msg)
