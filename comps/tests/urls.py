from __future__ import unicode_literals

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.conf.urls import include, url


handler404 = 'comps.tests.urls.test_404'
handler500 = 'comps.tests.urls.test_500'


def test_404(request):
    return HttpResponseNotFound()


def test_500(request):
    return HttpResponseServerError()


urlpatterns = [
    url(r'^comps/', include('comps.urls')),
]
