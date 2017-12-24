from django.db import models


class ShortURL(models.Model):
    """
    A model that describes URL entry in the DB
    """
    long_url = models.URLField("Original URL", null=True, blank=True)
    short_code = models.TextField("Short code", null=True, blank=True)
    created = models.DateTimeField("URL time of creation", auto_now_add=True)
    clicks = models.PositiveIntegerField("Clicks", null=False, default=0)

    class Meta:
        verbose_name = "Short URL"
        verbose_name_plural = "Short URLS"
        db_table = 'short_urls'

    def __str__(self):
        return f'{self.short_code} with {self.clicks} clicks'
