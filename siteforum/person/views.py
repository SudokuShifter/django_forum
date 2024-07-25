from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]

data_db = [{'id': 1, 'title': 'Пучан1',
            'content': 'Выпускник факультета автоматизированных систем и технологий Костромского государственного '
                       'технологического университета, направление «Информационные системы». С тех пор и являюсь '
                       'разработчиком ПО, использую в основном технологии Microsoft, главным образом — для Web. '
                       'Участвовал в IT-проектах различной сложности: от веб-сайтов городской администрации до '
                       'комплексных софтверных решений для израильских телекоммуникационных и финансовых компаний. '
                       'Больше 5 лет работал в группе компаний Softline, в том числе над проектом DeskWork.',
            'is_published': True},
           {'id': 2, 'title': 'Пучан2', 'content': 'Биография пучана2', 'is_published': False},
           {'id': 3, 'title': 'Пучан3', 'content': 'Биография пучана3', 'is_published': True}]


def index(request):
    # t = render_to_string('person/index.html')
    # return HttpResponse(t)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'person/index.html', context=data)


def about(request):
    return render(request, 'person/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id = {post_id}')


def addpage(request):
    return HttpResponse('Добавление статьи')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# def categories(request, cat_id):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_id}</p>')
#
#
# def categories_by_slug(request, cat_slug):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_slug}</p>')
#
#
# def archive(request, year):
#     if year > 2024:
#         """permanent=True - доп параметр для 301 редиректа"""
#         uri = reverse('cats', args=('sport', ))
#         return HttpResponsePermanentRedirect(uri)
#     return HttpResponse(f'<h1>Архив по категориям</h1><p>{year}</p>')


def page_not_found404(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def page_not_found500(request):
    return HttpResponse('<h1>Ошибка сервера</h1>', status=500)
