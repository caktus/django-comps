import os

from django.conf import settings
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist


def comp_listing(request, directory_slug=None):
    context = {}
    working_dir = settings.COMPS_DIR
    if directory_slug:
        working_dir = os.path.join(working_dir, directory_slug)
    dirnames = []
    templates = []
    items = os.listdir(working_dir)
    templates = [x for x in items if os.path.splitext(x)[1] == '.html']
    dirnames = [x for x in items if \
                    not os.path.isfile(os.path.join(working_dir, x))]
    templates.sort()
    dirnames.sort()
    context['directories'] = dirnames
    context['templates'] = templates
    context['subdirectory'] = directory_slug
    return render(request, "comps/comp_listing.html", context)


def comp(request, slug, directory_slug=None):
    context = {}
    path = settings.COMPS_DIR
    comp_dir = os.path.split(path)[1]
    template = "{0}/{1}".format(comp_dir, slug)
    if directory_slug:
        template = "{0}/{1}/{2}".format(comp_dir, directory_slug, slug)
    working_dir = os.path.join(path, slug)
    if os.path.isdir(working_dir):
        return redirect('comp-listing', directory_slug=slug)
    try:
        return render(request, template, context)
    except TemplateDoesNotExist:
        return redirect('comp-listing')
