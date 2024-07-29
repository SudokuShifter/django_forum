from django import template
import person.views as views
from person.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('person/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('person/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}
