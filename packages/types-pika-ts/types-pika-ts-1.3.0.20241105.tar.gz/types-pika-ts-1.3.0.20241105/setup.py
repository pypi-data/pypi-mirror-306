from setuptools import setup

name = "types-pika-ts"
description = "Typing stubs for pika"
long_description = '''
## Typing stubs for pika

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pika`](https://github.com/pika/pika) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pika`. This version of
`types-pika-ts` aims to provide accurate annotations for
`pika==1.3.*`.

The `types-pika` package contains alternate, more complete type stubs, that are maintained outside of typeshed.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pika`](https://github.com/python/typeshed/tree/main/stubs/pika)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.387,
and pytype 2024.10.11.
It was generated from typeshed commit
[`f314631fcbe80791a52c36123ba16a175b97ffa1`](https://github.com/python/typeshed/commit/f314631fcbe80791a52c36123ba16a175b97ffa1).
'''.lstrip()

setup(name=name,
      version="1.3.0.20241105",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pika.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pika-stubs'],
      package_data={'pika-stubs': ['__init__.pyi', 'adapters/__init__.pyi', 'adapters/asyncio_connection.pyi', 'adapters/base_connection.pyi', 'adapters/blocking_connection.pyi', 'adapters/gevent_connection.pyi', 'adapters/select_connection.pyi', 'adapters/tornado_connection.pyi', 'adapters/twisted_connection.pyi', 'adapters/utils/__init__.pyi', 'adapters/utils/connection_workflow.pyi', 'adapters/utils/io_services_utils.pyi', 'adapters/utils/nbio_interface.pyi', 'adapters/utils/selector_ioloop_adapter.pyi', 'amqp_object.pyi', 'callback.pyi', 'channel.pyi', 'compat.pyi', 'connection.pyi', 'credentials.pyi', 'data.pyi', 'delivery_mode.pyi', 'diagnostic_utils.pyi', 'exceptions.pyi', 'exchange_type.pyi', 'frame.pyi', 'heartbeat.pyi', 'spec.pyi', 'tcp_socket_opts.pyi', 'validators.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
