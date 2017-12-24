from django.contrib import admin
from django.urls import path

from apps.shortener.views import delete_url, info, redirect_to_url, submit_url, URLListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', submit_url, name='submit_url'),
    path('list/', URLListView.as_view(), name='list_urls'),
    path('info/<slug:short_code>', info, name='info'),
    path('delete/<slug:short_code>', delete_url, name='delete_url'),
    path('<slug:short_code>/', redirect_to_url, name='redirect_to_url')
]
