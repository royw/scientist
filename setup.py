# from distutils.core import setup
import json
import os
import re
from setuptools import setup

import sys

# Old style (not recommended) check to prevent setup.py from being used on old pythons.
# Current recommended practice is to include supported pythons in the
# classifiers kwarg even though there is no automated enforcement.
if sys.version_info < (2, 6):
    print('Science requires python 26 or newer')
    exit(-1)

#: str: Regular expression for parsing __version__ line in the packages __init__.py file.
VERSION_REGEX = r'__version__\s*=\s*[\'\"](\S+)[\'\"]'

# noinspection PyArgumentEqualDefault
def get_project_version():
    """
    Get the version from __init__.py with a line: /^__version__\s*=\s*(\S+)/
    If it doesn't exist try to load it from the VERSION.txt file.
    If still no joy, then return '0.0.0'

    :returns: the version string
    :rtype: str
    """

    # trying __init__.py first
    try:
        file_name = os.path.join(os.getcwd(), 'scientist', '__init__.py')
        # noinspection PyBroadException
        try:
            # python3
            with open(file_name, 'r', encoding='utf-8') as inFile:
                for line in inFile.readlines():
                    match = re.match(VERSION_REGEX, line)
                    if match:
                        return match.group(1)
        except:
            # python2
            with open(file_name, 'r') as inFile:
                for line in inFile.readlines():
                    match = re.match(VERSION_REGEX, line)
                    if match:
                        return match.group(1)
    except IOError:
        pass

    # no joy, so try getting the version from a VERSION.txt file.
    #    try:
    #        file_name = os.path.join(os.getcwd(), 'scientist', 'VERSION.txt')
    #        with open(file_name, 'r') as inFile:
    #            return inFile.read().strip()
    #    except IOError:
    #        pass

    # no joy again, so return default
    return '0.0.0'

#: List[str]: The list of the package names for runtime dependencies
required_imports = [
    'six',
    'fullmonty',
]

print("Python (%s)" % sys.version)

# libraries that have been moved into python are added to the list of runtime
# dependencies by python version.

if sys.version_info < (3, 1):
    required_imports.extend([
        'ordereddict',  # new in py31
        'decorator',
    ])

if sys.version_info < (3, 2):
    required_imports.extend([
        "argparse",  # new in py32
        "configparser",  # back port from py32
    ])

if sys.version_info < (3, 5):
    required_imports.extend([
#        "scandir",  # new in py35
    ])

#: str: the CLI templates support two descriptions, one brief and one long.
long_description = ""

# here we set the long_description to the contents of the README.rst file.
# noinspection PyBroadException
try:
    long_description = open('README.rst').read()
except:
    long_description = open('README.rst', encoding='utf-8').read()

kwargs = {}
if os.path.isfile('setup.json'):
    try:
        with open('setup.json') as data_file:
            kwargs = json.load(data_file)
    except Exception as ex:
        print("Unable to load setup.json - %s" % str(ex))

default_kwargs = {
    'name': 'Science',
    'version': get_project_version(),
    'author': 'Roy Wright',
    'author_email': 'roy.oti.wright@hpe.com',
    'url': 'http://scientist.example.com',
    'packages': ['scientist'],
    'package_dir': {'': '.'},
    'package_data': {'scientist': ['*.txt', '*.js', '*.html', '*.css'],
                     'tests': ['*'],
                     '': ['*.rst', '*.txt', '*.rc', '*.in']},
    'license': 'docs/license.rst',
    'description': "Port of python of github's ruby scientist.",
    'long_description': long_description,
    # use keywords relevant to the application
    'keywords': [],
    # use classifiers from:  https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'classifiers': [
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        # 'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
    ],
    'install_requires': required_imports,
    'entry_points': {
        'console_scripts': ['scientist = scientist.scientist_main:main']
    }
}

default_kwargs.update(kwargs)
setup(**default_kwargs)
