import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = (
    'pyramid',
    'voteit.core',
    'betahaus.pyracont',
    'betahaus.viewcomponent',
    'lingua',
    'Babel',
    'colander',
    'deform',
    )


setup(name='voteit.exportimport',
      version='0.1dev',
      description='VoteIT exports and imports',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Robin Harms Oredsson',
      author_email='robin@betahaus.net',
      url='http://www.voteit.se',
      keywords='web pylons pyramid voteit',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="voteit.exportimport",
      entry_points = """\
      """,
      message_extractors = { '.': [
              ('**.py',   'lingua_python', None ),
              ('**.pt',   'lingua_xml', None ),
              ]},
      )
