from django import forms
from django.core.validators import URLValidator

from .helpers import _schemes
from .models import ShortURL


class URLField(forms.URLField):
    """
    Overloading default URLField to accept all the URL's schemes out there
    """
    default_validators = [URLValidator(schemes=_schemes)]


class URLSubmitForm(forms.Form):
    """
    A form for long URL with custom error messages and custom attributes for input field
    """
    long_url = URLField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': "text",
                'class': "text-center form-control form-control-lg",
                'placeholder': "Вставьте сюда вашу ссылку",
            }
        ),
        error_messages={
            'invalid': 'Мы не уверены, что эта ссылка верна :(',
            'required': 'Нельзя сокртатить несократимое, пожалуйста, введите ссылку :)'
        }
    )

    class Meta:
        model = ShortURL
        fields = 'long_url'
