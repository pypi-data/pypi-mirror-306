from setuptools import setup

name = "types-flake8-bugbear"
description = "Typing stubs for flake8-bugbear"
long_description = '''
## Typing stubs for flake8-bugbear

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`flake8-bugbear`](https://github.com/PyCQA/flake8-bugbear) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `flake8-bugbear`. This version of
`types-flake8-bugbear` aims to provide accurate annotations for
`flake8-bugbear==24.10.31`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/flake8-bugbear`](https://github.com/python/typeshed/tree/main/stubs/flake8-bugbear)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.387,
and pytype 2024.10.11.
It was generated from typeshed commit
[`348c44f46830e69c1f3574ce8820f505134f9ca8`](https://github.com/python/typeshed/commit/348c44f46830e69c1f3574ce8820f505134f9ca8).
'''.lstrip()

setup(name=name,
      version="24.10.31.20241103",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-bugbear.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['bugbear-stubs'],
      package_data={'bugbear-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
