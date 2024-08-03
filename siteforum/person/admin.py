from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Person, Category


# Register your models here.

class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус мужчин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'photo', 'post_photo', 'cat', 'wife', 'tags']
    # exclude = ['tags', 'is_published']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ['tags']
    list_display = ('title', 'time_create', 'is_published', 'post_photo', 'cat')
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published', MarriedFilter]
    save_on_top = True

    @admin.display(description='Краткое описание', ordering='content')
    def breif_info(self, person: Person):
        return f'Описание {len(person.content)} символов'

    @admin.display(description='Фото', ordering='content')
    def post_photo(self, person: Person):
        if person.photo:
            return mark_safe(f'<img src ="{person.photo.url}" width=50>')
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Person.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Person.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

