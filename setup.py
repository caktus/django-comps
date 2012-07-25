import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='django-comps',
    version=__import__('comps').__version__,
    author='David Ray',
    author_email='davidray@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/daaray/django-comps',
    license='BSD',
    description=u' '.join(__import__('comps').__doc__.splitlines()).strip(),
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Environment :: Web Environment'
    ],
    long_description=read_file('README.md'),
)
