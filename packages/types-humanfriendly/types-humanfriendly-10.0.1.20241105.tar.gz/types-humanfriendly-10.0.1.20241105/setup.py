from setuptools import setup

name = "types-humanfriendly"
description = "Typing stubs for humanfriendly"
long_description = '''
## Typing stubs for humanfriendly

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`humanfriendly`](https://github.com/xolox/python-humanfriendly) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `humanfriendly`. This version of
`types-humanfriendly` aims to provide accurate annotations for
`humanfriendly==10.0.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/humanfriendly`](https://github.com/python/typeshed/tree/main/stubs/humanfriendly)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.387,
and pytype 2024.10.11.
It was generated from typeshed commit
[`f314631fcbe80791a52c36123ba16a175b97ffa1`](https://github.com/python/typeshed/commit/f314631fcbe80791a52c36123ba16a175b97ffa1).
'''.lstrip()

setup(name=name,
      version="10.0.1.20241105",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/humanfriendly.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['humanfriendly-stubs'],
      package_data={'humanfriendly-stubs': ['__init__.pyi', 'case.pyi', 'cli.pyi', 'compat.pyi', 'decorators.pyi', 'deprecation.pyi', 'prompts.pyi', 'sphinx.pyi', 'tables.pyi', 'terminal/__init__.pyi', 'terminal/html.pyi', 'terminal/spinners.pyi', 'testing.pyi', 'text.pyi', 'usage.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
