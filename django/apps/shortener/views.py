import logging

from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from urllib.parse import urlparse

from .forms import URLSubmitForm
from .helpers import _alphabet, _base
from .models import ShortURL

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)


class URLListView(ListView):
    """
    Pagination view class for short URLs
    """
    model = ShortURL
    template_name = 'shortener/urls_list.html'
    context_object_name = 'urls'
    paginate_by = 20
    queryset = ShortURL.objects.all().order_by('-clicks', '-created')


def encode(number):
    """
    Encodes PK to short URL code
    :param number: Positive integer that represents PK in the database
    :return: String that represents short URL code like 'ApRQT' in 'example.com/ApRQT'
    """
    short_code = ''
    while number > 0:
        short_code = _alphabet[number % _base] + short_code
        number //= _base
    return short_code


def is_valid(short_code):
    """
    Check if the code provided was built from our alphabet or not, and if it is empty or not
    :param short_code: String that represents short URL code like 'ApRQT' in 'example.com/ApRQT'
    :return: Boolean
    """
    if short_code and all(character in _alphabet for character in short_code):
        return True
    return False


def protocolify(user_url):
    """
    Check if user's URL contains a scheme, if not - adds default http://
    :param user_url: A string, entered by user
    :return: Processed string with scheme
    """
    parsed = urlparse(user_url)
    if not parsed.scheme:
        user_url = 'http://' + user_url
    return user_url


def submit_url(request):
    """
    URL input view. Checks if URL was POSTed, validates it, then checks if the URL points at our host, if not - tries to
    create an entry in the database. If the entry was created, encode it's PK into short code and show it to user. If it
    was not created - just pick the object and show the code generated earlier.
    :param request: Self-explanatory
    :return: Renders 200 or 400 with templates
    """
    this_host = request.META['HTTP_HOST']
    if request.method == "POST":
        form = URLSubmitForm(request.POST)
        if form.is_valid():
            user_url = form.data['long_url']
            if this_host in user_url:
                logging.debug('User tried to shorten an URL that points to our host, thrown 400')
                return render(request, 'shortener/bad_request.html', status=400)
            url_obj, created = ShortURL.objects.get_or_create(long_url=protocolify(user_url))
            if created:
                url_obj.short_code = encode(url_obj.pk)
                url_obj.save()
            return render(request, 'shortener/result.html', {'url_obj': url_obj, 'host': this_host})
    else:
        form = URLSubmitForm()
        url_objects = ShortURL.objects.all().order_by('-clicks', '-created')[:20]
    return render(request, 'shortener/index.html', {'form': form, 'urls': url_objects})


def info(request, short_code):
    """
    A view that retrieves URL's info like short code, long URL, clicks and date-time of creation
    :param request: Self-explanatory
    :param short_code: String that represents short URL code like 'ApRQT' in 'example.com/ApRQT'
    :return: Renders 200, 400 or 404 with templates
    """
    if is_valid(short_code):
        try:
            url_obj = ShortURL.objects.get(short_code=short_code)
            return render(request, 'shortener/url_info.html', {'url_obj': url_obj, 'host': request.META['HTTP_HOST']})
        except ShortURL.DoesNotExist:
            logging.debug('User tried to view the info for short URL that was not found in the database, thrown 404')
            return render(request, 'shortener/not_found.html', status=404)
    logging.debug('User tried to view info for invalid short URL, thrown 404')
    return render(request, 'shortener/bad_request.html', status=400)


def redirect_to_url(request, short_code):
    """
    A redirection view.
    :param request: Self-explanatory
    :param short_code: String that represents short URL code like 'ApRQT' in 'example.com/ApRQT'
    :return: Redirects to target long URL or renders 404 if user tries something funny
    """
    if is_valid(short_code):
        try:
            obj = ShortURL.objects.get(short_code=short_code)
            obj.clicks += 1
            obj.save()
            return redirect(obj.long_url, permanent=True)
        except ShortURL.DoesNotExist:
            logging.debug('User tried to access URL that was not found in the database, thrown 404')
            return render(request, 'shortener/not_found.html', status=404)
    else:
        logging.debug('User tried to access invalid short URL, thrown 404')
        return render(request, 'shortener/not_found.html', status=404)


def delete_url(request, short_code):
    """
    Short URL deletion view
    :param request: Self-explanatory
    :param short_code: String that represents short URL code like 'ApRQT' in 'example.com/ApRQT'
    :return: Redirects to previous page (URLs listing) or / if no referrer is provided, or renders 404 error if an URL
    was already deleted
    """
    if is_valid(short_code):
        try:
            obj = ShortURL.objects.get(short_code=short_code)
            obj.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except ShortURL.DoesNotExist:
            logging.debug('User tried to delete URL that was not found in the database, thrown 404')
            return render(request, 'shortener/not_found.html', status=404)
