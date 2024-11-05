# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umnet_db']

package_data = \
{'': ['*']}

install_requires = \
['netaddr>=1.3.0,<2.0.0',
 'psycopg2-binary>=2.9.9,<3.0.0',
 'python-decouple>=3.8,<4.0',
 'sqlalchemy>=2.0.24,<3.0.0',
 'texttable>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'umnet-db',
    'version': '0.1.0',
    'description': 'Custom database for storing network data',
    'long_description': '',
    'author': 'Amy Liebowitz',
    'author_email': 'amylieb@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
