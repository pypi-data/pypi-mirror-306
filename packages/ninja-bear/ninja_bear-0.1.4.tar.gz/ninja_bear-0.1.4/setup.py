from pathlib import Path
from setuptools import setup, find_packages

# Setup process taken from here: https://www.freecodecamp.org/news/build-your-first-python-package/.

DESCRIPTION = 'ninja-bear keeps your language specific constants in sync'
LONG_DESCRIPTION = Path(__file__).parent.absolute().joinpath('README.md').read_text('utf-8')

# Get version.
try:
    with open('src/ninja_bear/base/info.py') as fp:
        info = {}
        exec(fp.read(), info)
        VERSION = info['VERSION']
except Exception as e:
    print(e)
    exit(-1)

setup(
    name='ninja-bear', 
    version=VERSION,
    author='monstermichl',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['ninja_bear'],
    entry_points = {
        'console_scripts': ['ninja-bear=ninja_bear.cli:main'],
    },
    install_requires=[
        'pyyaml >= 6.0.1',
        'schema >= 0.7.5',
        'importlib-metadata >= 8.5.0',
    ],
    extras_require={
        'dev': [
            'wheel>=0.41.1',
            'twine>=4.0.2',
            'ruff>=0.0.47',
            'coverage>=7.2.7',
        ],
    },
    python_requires='>=3.10',
    classifiers= [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url = 'https://github.com/monstermichl/ninja-bear.git',
    keywords = [
        'ninja-bear',
        'constants',
        'language',
        'generator',
        'distributor',
    ],
)
