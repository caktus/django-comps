try:
    # Django 1.4+
    from django.conf.urls import url
except ImportError: # pragma: no cover
    # Django 1.3
    from django.conf.urls.defaults import url
from comps import views


urlpatterns = [
    url(r'^comps(?:/(?P<directory_slug>[\w\-]+))?/$',
        views.comp_listing,
        name='comp-listing'),
    url(r'^comps(?:/(?P<directory_slug>[\w\-]+))?/(?P<slug>[\w.\-]+)$',
        views.comp,
        name='comp'),
    url(r'^export-comps/$',
        views.export_comps,
        name='export-comps'),
]
