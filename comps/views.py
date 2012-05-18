import os

from django.conf import settings
from django.shortcuts import redirect, render


def comp_listing(request):
    context = {}
    comp_template_dir = '{0}/templates/comps/'.format(settings.PROJECT_PATH)
    templates = os.listdir(comp_template_dir)
    listing = 'comp_listing.html'
    templates = [x for x in templates if x != listing]
    templates.sort()
    context['templates'] = templates
    return render(request, "comps/{0}".format(listing), context)


def comp(request, slug):
    context = {}
    template = "comps/{0}".format(slug)
    try:
        return render(request, template, context)
    except:
        return redirect('comp-listing')
