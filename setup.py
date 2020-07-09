import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "notionmdimport",
    version = "0.0.1",
    author = "Abhijeet Rastogi",
    author_email = "abhijeet.1989@gmail.com",
    description = ("Uploads local markdown folder recursively to Notion.so"),
    license = "BSD",
    keywords = "markdown notion",
    url = "http://abhi.host",
    packages = find_packages(),
    long_description=read('README.md'),
    install_requires=[
        'click',
        'notion-py',
        'flake8',
        'md2notion',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-mock'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        "console_scripts": [
            "notionmdimport = notionmdimport.main:main"
        ],
    },
)
