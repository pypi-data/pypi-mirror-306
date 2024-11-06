# Django Fernet

[![PyPI](https://badge.fury.io/py/django-fernet.svg)](https://pypi.org/project/django-fernet/)
[![Test Status](https://github.com/anexia/django-fernet/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia/django-fernet/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/anexia/django-fernet/branch/main/graph/badge.svg)](https://codecov.io/gh/anexia/django-fernet)

A library that provides Django model fields to store value encrypted using Fernet.

## Installation

With a [correctly configured](https://pipenv.pypa.io/en/latest/basics/#basic-usage-of-pipenv) `pipenv` toolchain:

```bash
pipenv install django-fernet
```

You may also use classic `pip` to install the package:

```bash
pip install django-fernet
```

### Auto-formatter setup
We use ruff (https://github.com/astral-sh/ruff) for local auto-formatting and for linting in the CI pipeline.
The pre-commit framework (https://pre-commit.com) provides Git hooks for these tools, so they are automatically applied
before every commit.

Steps to activate:
* Install the pre-commit framework: `pip install pre-commit` (for alternative installation options
  see https://pre-commit.com/#install)
* Activate the framework (from the root directory of the repository): `pre-commit install`

Hint: You can also run the formatters manually at any time with the following command: `pre-commit run --all-files`


## Getting started

### Example model that defines fernet text fields

```python
from django.db import models
from django_fernet.fields import *


class ExampleTextModel(models.Model):
    example_field = FernetTextField(
        verbose_name="Example field",
    )
```

### Example model that defines fernet binary fields

```python
from django.db import models
from django_fernet.fields import *


class ExampleBinaryModel(models.Model):
    example_field = FernetBinaryField(
        verbose_name="Example field",
    )
```


## How to use

### Save encrypted text to the database

```python
from django_fernet.fernet import *

field_data = FernetTextFieldData()
field_data.encrypt("foo", "--secret--")

instance = ExampleTextModel()
instance.example_field = field_data
instance.save()
```

### Save encrypted binary data to the database

```python
from django_fernet.fernet import *

field_data = FernetTextFieldData()
field_data.encrypt(b"foo", "--secret--")

instance = ExampleBinaryModel()
instance.example_field = field_data
instance.save()
```

### Load encrypted text from the database

```python
instance = ExampleTextModel.objects.get(pk=...)
decrypted_str = instance.example_field.decrypt("--secret--")
```

### Load encrypted binary data from the database

```python
instance = ExampleBinaryModel.objects.get(pk=...)
decrypted_bytes = instance.example_field.decrypt("--secret--")
```


## Supported versions

|             | Django 4.2 | Django 5.0 | Django 5.1 |
|-------------|------------|------------|------------|
| Python 3.10 | ✓          | ✓          | ✓          |
| Python 3.11 | ✓          | ✓          | ✓          |
| Python 3.12 | ✓          | ✓          | ✓          |
| Python 3.13 | ✓          | ✓          | ✓          |
| PyPy 3.10   | ✓          | ✓          | ✓          |


## Tests

An example Django app that makes use of `django-fernet` can be found in the [tests/](tests/) folder. This example
Django app also contains the unit tests.

Follow below instructions to run the tests. You may exchange the installed Django version according to your
requirements.

```bash
# install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# run tests
cd tests && pytest
```


## List of developers

* Andreas Stocker <AStocker@anexia-it.com>
