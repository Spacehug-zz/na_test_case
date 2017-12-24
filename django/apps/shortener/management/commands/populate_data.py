import logging

from django.core.management.base import BaseCommand
from apps.shortener.models import ShortURL
from apps.shortener.views import encode, protocolify


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Adds test short URLs data to the database'
    websites = [
        'hh.ru',
        'www.google.com',
        'money.yandex.ru',
        'https://www.google.ru/search?q=%D0%BC%D1%8B%D1%88%D0%B8+%D0%B8%D1%85+%D1%81%D1%82%D0%BE%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C+%D0%B8+%D0%B3%D0%B4%D0%B5+%D0%BF%D1%80%D0%B8%D0%BE%D0%B1%D1%80%D0%B5%D1%81%D1%82%D0%B8&oq=%D0%9C%D1%8B%D1%88%D0%B8%2C+%D0%B8%D1%85+%D1%81%D1%82%D0%BE%D0%B8&aqs=chrome.1.69i57j0.2998j0j7&sourceid=chrome&ie=UTF-8',
        'http: // kaktam.ru /',
        'https://www.youtube.com/watch?v=lO9d-AJai8Q',
        'https://www.reddit.com/r/todayilearned/',
        'http://retailengineering.ru/normative-documentation/',
        'http://www.safestyle-windows.co.uk/secret-door/?dalek',
        'https://rutracker.org/forum/index.php',  # 10
        'https://www.duolingo.com/',
        'https://thepiratebay.org/',
        'https://en.wikipedia.org/wiki/Main_Page',
        'http://cs50.tv/2017/fall/',
        'http://waitbutwhy.com/',
        'https://github.com/serbernar/python_beginners_faq',
        'http://www.quickanddirtytips.com/',
        'http://neuralnet.info/',
        'http://www.pythonchallenge.com/pc/return/balloons.html',
        'http://cursivecole.fr/dico1.php',  # 20
        'http://flibusta.is/'
    ]

    def handle(self, *args, **options):
        for url in self.websites:
            logger.info(f'Creating an entry for {url}')
            url_obj, created = ShortURL.objects.get_or_create(long_url=protocolify(url))
            if created:
                url_obj.short_code = encode(url_obj.pk)
                url_obj.save()
        logger.info('Done populating test data')
