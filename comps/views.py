import os

from django.conf import settings
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist


def comp_listing(request, directory_slug=None):
    context = {}
    working_dir = settings.COMPS_DIR
    if directory_slug:
        working_dir = os.path.join(working_dir, directory_slug)
    templates = os.listdir(working_dir)
    listing = 'comp_listing.html'
    templates = [x for x in templates if x != listing]
    templates.sort()
    context['templates'] = templates
    context['subdirectory'] = directory_slug
    return render(request, "comps/{0}".format(listing), context)


def comp(request, slug, directory_slug=None):
    context = {}
    template = "comps/{0}".format(slug)
    if directory_slug:
        template = "comps/{0}/{1}".format(directory_slug, slug)
    working_dir = os.path.join(settings.COMPS_DIR, slug)
    if os.path.isdir(working_dir):
        return redirect('comp-listing', directory_slug=slug)
    try:
        return render(request, template, context)
    except TemplateDoesNotExist:
        return redirect('comp-listing')
