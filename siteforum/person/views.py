from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
import uuid

from django.views import View
from django.views.generic import TemplateView

from .forms import AddPostForm, UploadFileForm
from .models import Person, Category, TagPost, UploadFiles

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


class PersonHome(TemplateView):
    template_name = 'person/index.html'

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Person.published.all().select_related('cat'),
        'cat_selected': 0,
    }

    # Динамическое изменение словаря контекст для передачи каких-то данных через ПОСТ-запросы
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Person.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #
    #     return context


# Метод загрузки фотографий через чанки
# def handle_uploaded_file(f):
#     f_name, f_ex = f.name.split('.')
#     with open(f'uploads/{uuid.uuid4()}.{f_ex}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        # handle_uploaded_file(request.FILES['file_upload'])
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'person/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


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
        form = AddPostForm(request.POST, request.FILES)
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


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавить статью',
            'form': form,
        }
        return render(request, 'person/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
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
