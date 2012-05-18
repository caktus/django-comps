from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^comps$', 'comp_listing', name='comp-listing'),
    url(r'^comps/(?P<slug>[\w.\-]+)$', 'comp', name='comp'),
)
