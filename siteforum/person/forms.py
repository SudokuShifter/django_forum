from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible


from .models import Category, Wife, Person


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    """
    Вариант заполнения формы
    title = forms.CharField(max_length=255, min_length=5,
                            label='Заголовок', error_messages= {'min_length': 'Короткий заголовок',
                                                                'required': 'Без заголовка никак'},
                            validators=[
                                RussianValidator(),
                            ],
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов'),
                           ])
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Содержание')
    is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    """
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Не выбрана', label='Категория')
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(),
                                  required=False, empty_label='Не женат', label='Супруга')

    class Meta:
        model = Person
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'wife', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'forms': 5}),
        }
        labels = {
            'is_published': 'Статус',
            'slug': 'URL',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title

    """
    Вариант валидации поля формы
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только русские символы, дефис и пробел')
    """