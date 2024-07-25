from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string


def index(request):
    # t = render_to_string('person/index.html')
    # return HttpResponse(t)
    return render(request, 'person/index.html')


def about(request):
    return render(request, 'person/about.html')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_id}</p>')


def categories_by_slug(request, cat_slug):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_slug}</p>')


def archive(request, year):
    if year > 2024:
        """permanent=True - доп параметр для 301 редиректа"""
        uri = reverse('cats', args=('sport', ))
        return HttpResponsePermanentRedirect(uri)
    return HttpResponse(f'<h1>Архив по категориям</h1><p>{year}</p>')


def page_not_found404(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def page_not_found500(request):
    return HttpResponse('<h1>Ошибка сервера</h1>', status=500)