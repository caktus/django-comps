from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('comps.views',
    url(r'^comps/$', 'comp_listing', name='comp-listing'),
    url(r'^comps/(?P<slug>[\w.\-]+)$', 'comp', name='comp'),
)
