# Generated by Django 4.2.1 on 2025-06-28 21:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0009_husband_m_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads_model')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='women',
            options={'ordering': ['-time_created'], 'verbose_name': 'Известная женщина', 'verbose_name_plural': 'Известные женщины'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='women',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='women.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='women',
            name='content',
            field=models.TextField(blank=True, verbose_name='Текст статьи'),
        ),
        migrations.AlterField(
            model_name='women',
            name='husband',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wuman', to='women.husband', verbose_name='Муж'),
        ),
        migrations.AlterField(
            model_name='women',
            name='is_published',
            field=models.BooleanField(choices=[(False, 'Черновик'), (True, 'Опубликовано')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='women',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов'), django.core.validators.MaxLengthValidator(100, message='Максимум 100 символов')], verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='women',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='women.tagpost', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='women',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='women',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='women',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]
