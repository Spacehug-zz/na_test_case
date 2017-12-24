from django.contrib import admin
from django.contrib.auth.models import User, Group
from rangefilter.filter import DateRangeFilter

from .models import ShortURL


class URLClicksFilter(admin.SimpleListFilter):
    """
    A filter to view the urls that were clicked at least once, the urls tat were not, and all of the urls
    """
    title = "times clicked"
    parameter_name = 'urls_clicked'

    def lookups(self, request, model_admin):
        return (False, "Never"), (True, "At least once")

    def queryset(self, request, queryset):
        return queryset


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    """
    Short URL administration
    Does not allow to edit anything but link clicks
    """
    list_display = 'pk', 'short_code', 'created', 'clicks', 'long_url'
    ordering = 'pk', 'clicks', 'created'
    list_display_links = 'pk', 'short_code', 'created', 'clicks', 'long_url'
    list_filter = (URLClicksFilter, ('created', DateRangeFilter))
    search_fields = 'pk', 'short_code', 'created', 'clicks', 'long_url'
    readonly_fields = ('short_code', 'created', 'long_url')
    empty_value_display = '-----'

    class Meta:
        model = ShortURL

    def has_add_permission(self, request):
        return False


# We don't need these at all
admin.site.unregister(User)
admin.site.unregister(Group)
