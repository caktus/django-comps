import sys
import os

from io import BytesIO

from zipfile import ZipFile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import get_template, render_to_string

PY2 = sys.version_info[0] == 2


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
        t = get_template(template)
    except TemplateDoesNotExist:
        return redirect('comp-listing')

    c = RequestContext(request, context)
    return HttpResponse(t.render(c))


def export_comps(request):
    """
    Returns a zipfile of the rendered HTML templates in the COMPS_DIR
    """
    in_memory = BytesIO()
    zip = ZipFile(in_memory, "a")

    comps = settings.COMPS_DIR
    static = settings.STATIC_ROOT or ""
    context = RequestContext(request, {})
    context['debug'] = False

    # dump static resources
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
                # convert static refs to relative links
                dotted_rel = os.path.relpath(static, full_path)
                new_rel_path = '{0}{1}'.format(dotted_rel, '/static')
                content = content.replace(b'/static', bytes(new_rel_path, 'utf8'))
            path = os.path.join('static', rel_path)
            zip.writestr(path, content)

    for dirname, dirs, filenames in os.walk(comps):
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            rel_path = os.path.relpath(full_path, comps)
            template_path = os.path.join(comps.split('/')[-1], rel_path)
            html = render_to_string(template_path, context)
            # convert static refs to relative links
            depth = len(rel_path.split(os.sep)) - 1
            if depth == 0:
                dotted_rel = '.'
            else:
                dotted_rel = ''
                i = 0
                while i < depth:
                    dotted_rel += '../'
                    i += 1
            new_rel_path = '{0}{1}'.format(dotted_rel, '/static')
            html = html.replace('/static', new_rel_path)
            if PY2:
                html = unicode(html)
            zip.writestr(rel_path, html.encode('utf8'))

    for item in zip.filelist:
        item.create_system = 0
    zip.close()

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=comps.zip"
    in_memory.seek(0)
    response.write(in_memory.read())

    return response
