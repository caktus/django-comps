django-comps
==========================

An app that facilitates rapid prototyping.

Provides an entry point for deeper integration of naive-to-Django front end designers into a project.

Install
-------

``pip install django-comps``

Add ``comps`` to your ``INSTALLED_APPS``

Configure the path to your ``COMPS_DIR``

```
#Designate the folder for comp/design work
COMPS_DIR = '/path/to/project/templates/comps'
```

Configure **urls.py**

```
if 'comps' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^', include('comps.urls')))
```

Usage
-------
Protypes can be built in the ``COMPS-DIR`` and render within he context of
a Django project, without the need for defined views.

* Take advantage of the templating engine
* No need to pre-configure urls and views during prototyping
* Onboard new designers to the wonders of Django

Plumbing
--------

* ``/comps`` renders a list of ** *.html ** files and directories located within the ``COMPS_DIR``
* ``/comp/*.html`` renders the template in question.

