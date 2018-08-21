.. norfs documentation master file, created by
   sphinx-quickstart on Tue Dec 12 18:59:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:


norfs
=====

**Nor**\ malized **f**\ ile\ **s**\ ystem. This library offers a common interface to interact with multiple filesystems,
local or remote::

    import norfs.helpers

    local = norfs.helpers.local()
    demo_file = local.file('demo.txt')
    demo_file.write(b'Hello World')
    print(demo_file.read())


Installation
============
Install with ``pip``: ``pip install norfs``.

For python 3.4 and 3.5 you can install ``pip install norfs-py3.4``.

You can also download the source code from the `git repository`_.

.. _git repository: https://github.com/Galbar/norfs


Supported Filesystems
=====================
* `Local filesystem`_
* S3_
* In-memory_

The library is easily extensible! If you want a new filesystem supported implement it yourself or `create an issue`_.

.. _create an issue: https://github.com/Galbar/norfs/issues

Local filesystem
----------------

Implements the norfs contract to work with files and directories in the local filesystem::

    import norfs.helpers

    local = norfs.helpers.local()

    my_directory = local.dir("/my/local/directory")
    my_file = local.file("/my/local/file.txt")

S3
--

Implements the norfs contract to work with files and directories in an S3 compatible store::

    import norfs.helpers
    import boto3

    s3 = norfs.helpers.s3(s3_client=boto3.client("s3"))

    my_directory = s3.dir("myBucket/my/s3/directory")
    my_file = s3.file("myBucket/my/s3/file.txt")

In-memory
---------

Implements the norfs contract to work with files and directories in a very simple in-memory filesystem::

    import norfs.helpers

    memory = norfs.helpers.memory()

    my_directory = memory.dir("/my/memory/directory")
    my_file = memory.file("/my/memory/file.txt")


The norfs interface
===================

The most public interface norfs exposes is composed of the Clients_, the `Filesystem objects`_ and the `helpers
module`_.

Clients
-------

.. automodule:: norfs.client
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Filesystem objects
-------------------

.. automodule:: norfs.filesystem
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Helpers module
--------------

.. automodule:: norfs.helpers
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. toctree::
   :hidden:

   index
   examples
   norfs
