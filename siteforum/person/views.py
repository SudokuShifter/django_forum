from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .forms import AddPostForm
from .models import Person, Category, TagPost

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    posts = Person.published.all().select_related('cat')
    # t = render_to_string('person/index.html')
    # return HttpResponse(t)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'person/index.html', context=data)


def about(request):
    return render(request, 'person/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Person, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'person/post.html', data)


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            """
            Вариант сохранения данных в БД
            try:
                Person.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
            """
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    data = {
        'menu': menu,
        'title': 'Добавить статью',
        'form': form,
    }
    return render(request, 'person/addpage.html', data)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


"""
Работа со SlUG и Редирект (редирект 301 - постоянный переезд адреса, 302 - временный)

def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_id}</p>')


def categories_by_slug(request, cat_slug):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_slug}</p>')


def archive(request, year):
    if year > 2024:
        # permanent=True - доп параметр для 301 редиректа
        uri = reverse('cats', args=('sport', ))
        return HttpResponsePermanentRedirect(uri)
    return HttpResponse(f'<h1>Архив по категориям</h1><p>{year}</p>')
"""


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Person.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'person/index.html', data)


def show_tag_post_list(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Person.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'person/index.html', context=data)


def page_not_found404(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def page_not_found500(request):
    return HttpResponse('<h1>Ошибка сервера</h1>', status=500)
