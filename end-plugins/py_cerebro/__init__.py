# -*- coding: utf-8 -*-

"""
py_cerebro package contains modules that provide program interface for file storage (Cargador) and database.

The package includes the following modules:

* :py:mod:`py_cerebro.database` -- access to the database to execute :ref:`SQL-queries <sapi-sql>`.
* :py:mod:`py_cerebro.dbtypes` --  describes the data tuples of the bit flags used when working with the database.
* :py:mod:`py_cerebro.cargador` -- Access to the Cargador file storage.
* :py:mod:`py_cerebro.cclib` -- Contains auxiliary functions for handling hashes and bit flags.
"""

__all__ = ["database", "cargador", "dbtypes", "cclib"]
from py_cerebro import *
 