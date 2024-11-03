# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base4']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['base4 = base4.cli:main']}

setup_kwargs = {
    'name': 'base4',
    'version': '0.4.1',
    'description': 'base4 Encoder/Decoder',
    'long_description': '# Python base4\n\nA Python module to encode/decode binary data using base4 as described in [RFC 9285 ](https://www.rfc-editor.org/info/rfc9285).\n',
    'author': 'NasrPy',
    'maintainer': None,
    'maintainer_email': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
