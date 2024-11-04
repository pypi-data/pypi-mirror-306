# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chronometrage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chronometrage',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Pierre Lemaitre',
    'author_email': 'oultetman@sfr.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
