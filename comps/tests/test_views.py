import StringIO
import os
import zipfile

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import unittest


class CompsViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        #setup testing template path
        cwd = os.path.dirname(__file__)
        path_parts = cwd.split(os.sep)[:-1]
        base_path = os.path.join(*path_parts)
        settings.COMPS_DIR = os.path.join(os.sep, base_path,
                                         'templates', 'comps_test')

    def test_comp_listing(self):
        """
        render the listing template
        """
        response = self.client.get(reverse('comp-listing'))
        templates = response.context['templates']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(templates), 2)
        self.assertEqual(len(response.context['directories']), 1)

    def test_comp_subdirectory_listing(self):
        """
        render the listing template for a subdirectory
        """
        response = self.client.get(reverse('comp-listing',
                                            args=['subdirectory'])
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['templates']), 1)
        self.assertEqual(response.context['directories'], [])

    def test_comp_html_template(self):
        """
        Render the template
        """
        response = self.client.get(reverse('comp', args=['foo.html']))
        self.assertEqual(response.status_code, 200)

    def test_comp_no_template(self):
        """
        Redirect to comp_listing if the template does not exist
        """
        response = self.client.get(reverse('comp', args=['nothing']))
        self.assertEqual(response.status_code, 302)

    def test_zip_export(self):
        """
        Ensure all of the templates were exported
        """
        files = ['foo.html', 'bar.html', 'subdirectory/foo.html']
        response = self.client.get(reverse('export-comps'))
        self.assertEqual(response.status_code, 200)
        zf = zipfile.ZipFile(StringIO.StringIO(response.content))
        zf_filenames = [x.filename for x in zf.filelist]
        self.assertEqual(len(zf_filenames), len(files))
        matches = set(zf_filenames) & set(files)
        self.assertEqual(len(matches), 3)
