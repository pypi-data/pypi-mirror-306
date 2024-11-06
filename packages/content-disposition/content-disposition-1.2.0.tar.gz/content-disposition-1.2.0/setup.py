import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="content-disposition",
    version=os.getenv("PACKAGE_VERSION", "0.0.0").replace("refs/tags/", ""),
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description='A library that allows easy management of "Content-Disposition" details of HTTP responses.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/anexia/python-content-disposition",
    author="Alexandra Bruckner",
    author_email="abruckner@anexia-it.com",
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
