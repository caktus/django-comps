import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import NoArgsCommand, CommandError
from django.template import RequestContext
from django.template.loader import render_to_string
from django.test.client import RequestFactory


class Command(NoArgsCommand):
    help = 'Exports current comps directory as static HTML pages.'

    def handle_noargs(self, **options):
        comps = getattr(settings, 'COMPS_DIR', None)
        if comps is None:
            raise CommandError('Missing COMPS_DIR setting')
        output = os.path.join(comps, os.pardir, 'output')
        if not os.path.exists(output):
            os.mkdir(output)
        request = RequestFactory().get('/')
        context = RequestContext(request, {})
        context['STATIC_URL'] = './static/'
        context['debug'] = False
        settings.STATIC_ROOT = os.path.join(output, 'static')
        for dirname, dirs, filenames in os.walk(comps):
            for filename in filenames:
                full_path = os.path.join(dirname, filename)
                rel_path = os.path.relpath(full_path, comps)
                template_path = os.path.join('comps', rel_path)
                rendered = render_to_string(template_path, context)
                result = os.path.join(output, rel_path)
                with open(result, 'w') as f:
                    f.write(rendered)
        call_command('collectstatic', interactive=False)
