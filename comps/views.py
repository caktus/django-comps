import os

from StringIO import StringIO
from zipfile import ZipFile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist
from django.template import RequestContext
from django.template.loader import render_to_string


def comp_listing(request, directory_slug=None):
    """
    Output the list of HTML templates and subdirectories in the COMPS_DIR
    """
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
    """
    View the requested comp
    """
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


def export_comps(request):
    """
    Returns a zipfile of the rendered HTML templates in the COMPS_DIR
    """
    in_memory = StringIO()
    zip = ZipFile(in_memory, "a")

    comps = settings.COMPS_DIR
    static = settings.STATIC_ROOT
    media = settings.MEDIA_ROOT
    context = RequestContext(request, {})
    context['debug'] = False

    # dump static/mediaresources
    # TODO: inspect each template and only pull in resources that are used
    for dirname, dirs, filenames in os.walk(static):
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            rel_path = os.path.relpath(full_path, static)
            content = open(full_path, 'rb').read()
            try:
                ext = os.path.splitext(filename)[1]
            except IndexError:
                pass
            if ext == '.css':
                # convert static and media refs to relative links
                for directory in ['/static', '/media']:
                    dotted_rel = os.path.relpath(static, full_path)
                    new_rel_path = '{0}{1}'.format(dotted_rel, directory)
                    content = content.replace(directory, new_rel_path)
            path = os.path.join('static', rel_path)
            zip.writestr(path, content)

# We should not need media files in this context
#    for dirname, dirs, filenames in os.walk(media):
#        for filename in filenames:
#            full_path = os.path.join(dirname, filename)
#            rel_path = os.path.relpath(full_path, media)
#            content = open(full_path, 'rb').read()
#            path = os.path.join('media', rel_path)
#            zip.writestr(path, content)

    for dirname, dirs, filenames in os.walk(comps):
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            rel_path = os.path.relpath(full_path, comps)
            template_path = os.path.join(comps.split('/')[-1], rel_path)
            html = render_to_string(template_path, context)
            # convert static and media refs to relative links
            for directory in ['/static', '/media']:
                depth = len(rel_path.split(os.sep)) - 1
                if depth == 0:
                    dotted_rel = '.'
                else:
                    dotted_rel = ''
                    i = 0
                    while i < depth:
                        dotted_rel += '../'
                        i += 1
                new_rel_path = '{0}{1}'.format(dotted_rel, directory)
                html = html.replace(directory, new_rel_path)
            zip.writestr(rel_path, unicode(html).encode("utf8"))

    for item in zip.filelist:
        item.create_system = 0
    zip.close()

    response = HttpResponse(mimetype="application/zip")
    response["Content-Disposition"] = "attachment; filename=comps.zip"
    in_memory.seek(0)
    response.write(in_memory.read())

    return response
