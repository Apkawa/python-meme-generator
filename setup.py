# !/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

version = "0.0.0"

if sys.argv[-1] == "publish":
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system("rm -rf dist/")
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

if sys.argv[1] == "bumpversion":
    print("bumpversion")
    try:
        part = sys.argv[2]
    except IndexError:
        part = "patch"

    os.system("bumpversion --config-file setup.cfg %s" % part)
    sys.exit()

__doc__ = ""

project_name = "python-meme-generator"
app_name = "meme_generator"

ROOT = os.path.dirname(__file__)


def read(fname):
    return open(os.path.join(ROOT, fname)).read()


setup(
    name=project_name,
    version=version,
    description=__doc__,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/Apkawa/%s" % project_name,
    author="Apkawa",
    author_email="apkawa@gmail.com",
    packages=[package for package in find_packages() if package.startswith(app_name)],
    python_requires=">=3.5, <4",
    install_requires=["pycairo", "PyGObject", "webcolors", "pillow", "click"],
    zip_safe=False,
    include_package_data=True,
    keywords=[""],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
