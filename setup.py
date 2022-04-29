# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol_script_languages_container_ci',
 'exasol_script_languages_container_ci.cli',
 'exasol_script_languages_container_ci.cli.commands',
 'exasol_script_languages_container_ci.lib']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.0',
 'click>=8.0.3,<9.0.0',
 'exasol-integration-test-docker-environment @ '
 'https://github.com/exasol/integration-test-docker-environment/releases/download/0.10.0/exasol_integration_test_docker_environment-0.10.0-py3-none-any.whl',
 'exasol_script_languages_container_tool @ '
 'https://github.com/exasol/script-languages-container-tool/releases/download/0.12.0/exasol_script_languages_container_tool-0.12.0-py3-none-any.whl']

setup_kwargs = {
    'name': 'exasol-script-languages-container-ci',
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
