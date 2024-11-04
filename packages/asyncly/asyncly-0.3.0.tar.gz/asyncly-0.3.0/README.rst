Asyncly
=======

.. image:: https://img.shields.io/pypi/v/asyncly.svg
   :target: https://pypi.python.org/pypi/asyncly/
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/base-http-client.svg
   :target: https://pypi.python.org/pypi/base-http-client/

.. image:: https://img.shields.io/pypi/pyversions/base-http-client.svg
   :target: https://pypi.python.org/pypi/base-http-client/

.. image:: https://img.shields.io/pypi/l/base-http-client.svg
   :target: https://pypi.python.org/pypi/base-http-client/

Simple HTTP client and server for your integrations based on aiohttp_.

Installation
------------

Installation is possible in standard ways, such as PyPI or
installation from a git repository directly.

Installing from PyPI_:

.. code-block:: bash

   pip install asyncly

Installing from github.com:

.. code-block:: bash

   pip install git+https://github.com/andy-takker/asyncly

The package contains several extras and you can install additional dependencies
if you specify them in this way.

For example, with msgspec_:

.. code-block:: bash

   pip install "asyncly[msgspec]"

Complete table of extras below:

+-------------------------------------+----------------------------------+
| example                             | description                      |
+========================================================================+
| ``pip install "asyncly[msgspec]"``  | For using msgspec_ structs       |
+-------------------------------------+----------------------------------+
| ``pip install "asyncly[orjson]"``   | For fast parsing json by orjson_ |
+-------------------------------------+----------------------------------+
| ``pip install "asyncly[pydantic]"`` | For using pydantic_ models       |
+-------------------------------------+----------------------------------+

Quick start guide
-----------------

BaseHttpClient
~~~~~~~~~~~~~~

Simple HTTP Client for `https://catfact.ninja`. See full example in `examples/catfact_client.py`_

.. code-block:: python

   from base_http_client.client import (
       DEFAULT_TIMEOUT,
       BaseHttpClient,
       ResponseHandlersType,
   )
   from base_http_client.handlers.pydantic import parse_model
   from base_http_client.timeout import TimeoutType


   class CatfactClient(BaseHttpClient):
       RANDOM_CATFACT_HANDLERS: ResponseHandlersType = MappingProxyType(
            {
                 HTTPStatus.OK: parse_model(CatfactSchema),
            }
       )

      async def fetch_random_cat_fact(
          self,
          timeout: TimeoutType = DEFAULT_TIMEOUT,
      ) -> CatfactSchema:
          return await self._make_req(
              method=hdrs.METH_GET,
              url=self._url / "fact",
              handlers=self.RANDOM_CATFACT_HANDLERS,
              timeout=timeout,
          )




.. _PyPI: https://pypi.org/
.. _aiohttp: https://pypi.org/project/aiohttp/
.. _msgspec: https://github.com/jcrist/msgspec
.. _orjson: https://github.com/ijl/orjson
.. _pydantic: https://github.com/pydantic/pydantic

.. _examples/catfact_client.py: https://github.com/andy-takker/asyncly/blob/master/examples/catfact_client.py