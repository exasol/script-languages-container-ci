# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_languages_container_ci',
 'script_languages_container_ci.cli',
 'script_languages_container_ci.cli.commands',
 'script_languages_container_ci.lib']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.0',
 'click>=8.0.3,<9.0.0',
 'exasol-script-languages-container-tool @ '
 'git+https://github.com/exasol/script-languages-container-tool.git@feature/121_install_starter_scripts_via_python']

setup_kwargs = {
    'name': 'script-languages-container-ci',
    'version': '0.1.0',
    'description': 'Implements CI builds for script-language-container.',
    'long_description': None,
    'author': 'Thomas Uebensee',
    'author_email': 'ext.thomas.uebensee@exasol.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
