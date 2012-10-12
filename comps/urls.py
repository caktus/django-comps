from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('comps.views',
    url(r'^comps(?:/(?P<directory_slug>[\w\-]+))?/$',
        'comp_listing',
        name='comp-listing'),
    url(r'^comps(?:/(?P<directory_slug>[\w\-]+))?/(?P<slug>[\w.\-]+)$',
        'comp',
        name='comp'),
    url(r'^export-comps/$',
        'export_comps',
        name='export-comps'),
)
