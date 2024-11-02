# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.dataprofiles']

package_data = \
{'': ['*']}

install_requires = \
['mojo-errors>=2.0.0,<2.1.0',
 'mojo-interfaces>=2.0.1,<2.1.0',
 'pyyaml>=6.0.2,<7.0.0']

setup_kwargs = {
    'name': 'mojo-dataprofiles',
    'version': '2.0.2',
    'description': 'Automation Mojo Data Profiles Package',
    'long_description': '=====================================\nAutomation Mojo Data Profiles Package\n=====================================\nThis package provides a means for managing the information associated with data source profiles.\n\n=================\nCode Organization\n=================\n* .vscode - Common tasks\n* development - This is where the runtime environment scripts are located\n* repository-setup - Scripts for homing your repository and to your checkout and machine setup\n* userguide - Where you put your user guide\n* source/packages - Where the python namespace packages are located.\n* workspaces - This is where you add VSCode workspaces templates and where workspaces show up when homed.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n',
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
