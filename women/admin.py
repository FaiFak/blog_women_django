from django.contrib import admin, messages
from .models import Women
from .models import Category


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags']
    # readonly_fields = ['slug']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ['title', 'time_created', 'is_published', 'cat', 'brief_info']
    list_display_links = ('title',)
    ordering = ['title']
    list_editable = ('is_published',)
    list_per_page = 6
    actions = ['set_published', 'set_draft']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    search_fields = ['title', 'cat__name']

    # Пользовательские поля
    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов"

    # Пользовательские действия
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Записей изменено: {count} записей.")

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Количество записей, снятых с публикации: {count}.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ('id', 'name')
