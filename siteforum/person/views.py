from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Страница приложения person')


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_id}</p>')


def categories_by_slug(request, cat_slug):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{cat_slug}</p>')


def archive(request, year):
    return HttpResponse(f'<h1>Архив по категориям</h1><p>{year}</p>')