Getting Started
====================================

Below are the basic steps need to get django-comps integrated into your
Django project.


Configure Settings
------------------------------------

You need to include ``comps`` to your installed apps.

.. code-block:: python

    INSTALLED_APPS = (
        # Other installed apps would go here
        'comps',
    )


django-comps inspects the contents of a template directory. Configure the path
for the directory you will be storing your design/prototyping work:

.. code-block:: python

    COMPS_DIR = '/path/to/project/templates/comps'


Configure Urls
------------------------------------

You should include the comps urls in your root url patterns.

.. code-block:: python

    if 'comps' in settings.INSTALLED_APPS:
        urlpatterns += patterns('', url(r'^', include('comps.urls')))

That should be enough to get you up and running with django-comps.
