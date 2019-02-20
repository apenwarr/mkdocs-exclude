import os.path
import setuptools
from setuptools import setup

def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name='mkdocs-exclude',
    version='1.0.2',
    packages=['mkdocs_exclude'],
    url='https://github.com/apenwarr/mkdocs-exclude',
    license='Apache',
    author='Avery Pennarun',
    author_email='apenwarr@gmail.com',
    description='A mkdocs plugin that lets you exclude files or trees.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['mkdocs'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        'mkdocs.plugins': [
            'exclude = mkdocs_exclude:Exclude',
        ]
    },
)
