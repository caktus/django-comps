import os
from django.utils import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings



class CompsViewsTestCase(unittest.TestCase):


    def setUp(self):
        self.client = Client()
        cwd = os.path.dirname(__file__)
        settings.COMPS_DIR = os.path.join(cwd, 'templates/comps_test')

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
