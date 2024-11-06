# Content Disposition

[![PyPI version](https://img.shields.io/pypi/v/content-disposition.svg)](https://pypi.org/project/content-disposition/)
[![Run linter and tests](https://github.com/anexia/python-content-disposition/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia/python-content-disposition/actions/workflows/test.yml)
[![Codecov](https://img.shields.io/codecov/c/gh/anexia/python-content-disposition)](https://codecov.io/gh/anexia/python-content-disposition)

A library that allows easy management of 'Content-Disposition' details of HTTP responses.

So far it provides:
* RFC 5987 (file response, https://datatracker.ietf.org/doc/html/rfc5987)

## Installation

1. Install using pip:

```
pip install content-disposition
```

## Usage

Use the rfc5987_content_disposition function to set an HTTP response's 'Content-Type' field in any endpoint, e.g.:
```
# within views.py

from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from content_disposition import rfc5987_content_disposition

class MyViewSet(viewsets.ModelViewSet):
    ...

    @action(
        detail=True,
        methods="get",
        url_path=r"download",
    )
    def download_route(self, request, pk=None):
        """
        Assuming that self.get_object() returns a model defining
        'name = models.CharField(...)', 'file = models.FileField(...)' and 'mime = models.CharField(...)'
        whereas 'mime' represents the correct mime_type related to 'file'
        """
        instance = self.get_object()

        response = FileResponse(
            instance.file,
            content_type=instance.mime,
        )
        response["Content-Disposition"] = rfc5987_content_disposition(instance.name)

        return response
    ...
```

## Run tests in PyCharm

The package comes with a Django test app to verify functionalities in a realistic environment. To locally run the
provided test cases, e.g. in your IntelliJ IDEA, you can:

1. Configure the interpreter
   1. Go to `File` -> `Settings` -> `Project: content-disposition` -> `Python interpreter`
   2. `Add` a `Virtualenv Environment` and configure the correct `Location` and check `Inherit global site-packages`:
      1. ![python interpreter config](/docs/pycharm_python_interpreter_config.png)
2. Configure the Django framework
   1. Go to `File` -> `Settings` -> `Languages & Frameworks` -> `Django`
   2. Check `Enable Django Support` and configure the correct project root, settings and manage script location:
      1. ![django_config](/docs/pycharm_library_config.png)
3. Install the requirements by running: `pip install -r requirements.txt` in a terminal within your venv
4. Right click on the `tests` folder and select `Run 'Test:'`
5. The "Run" window should list all (successfully) executed test cases:
   1. ![test_results](/docs/pycharm_test_results.png)
