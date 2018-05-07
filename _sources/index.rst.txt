.. norfs documentation master file, created by
   sphinx-quickstart on Tue Dec 12 18:59:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _index:


norfs
=====

**Nor**\ malized **f**\ ile\ **s**\ ystem. This library offers a common interface to interact with multiple filesystems,
local or remote.


Installation
============
Install with ``pip``: ``pip install norfs``.

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

    import norfs

    my_directory = norfs.localdir("/my/local/directory")
    my_file = norfs.localfile("/my/local/file.txt")

S3
--

Implements the norfs contract to work with files and directories in an S3 compatible store::

    import norfs
    import boto3

    norfs.configure(s3_client=boto3.client("s3"))

    my_directory = norfs.s3dir("myBucket/my/s3/directory")
    my_file = norfs.s3file("myBucket/my/s3/file.txt")
    # or
    my_directory = norfs.s3dir("myBucket", "my/s3/directory")
    my_file = norfs.s3file("myBucket", "my/s3/file.txt")

In-memory
---------

Implements the norfs contract to work with files and directories in a very simple in-memory filesystem::

    import norfs

    my_directory = norfs.memorydir("/my/memory/directory")
    my_file = norfs.memoryfile("/my/memory/file.txt")



The norfs interface
===================

The most public interface norfs exposes is the BaseFileSystemObject_ and its subclasses Directory_ an File_.

BaseFileSystemObject
--------------------

``BaseFileSystemObject`` represents any object in the filesystem. It is the most abstract representation.

A ``BaseFileSystemObject`` exposes the following interface:

``.as_dir()`` -> Directory_
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns itself as a Directory instance or raises a ``NotADirectoryError``.

``.as_file()`` -> File_
~~~~~~~~~~~~~~~~~~~~~~~
Returns itself as a File instance or raises a ``NotAFileError``.

``.copy(`` destination: BaseFileSystemObject_ ``)`` -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Copy this to destination.

If source is a Directory_ and destination is a File_ it raises a ``TypeError``.

On copy failure it raises a ``FileSystemOperationError``.

``.exists()`` -> bool
~~~~~~~~~~~~~~~~~~~~~
Returns whether self exists in the file system.

``.is_dir()`` -> bool
~~~~~~~~~~~~~~~~~~~~~
Returns whether self is a Directory_.

``.is_file()`` -> bool
~~~~~~~~~~~~~~~~~~~~~~
Returns whether self is a File_.

``.name``: str
~~~~~~~~~~~~~~
The name of self.

``.parent()`` -> Directory_
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Return parent Directory_ of self.

``.path``: str
~~~~~~~~~~~~~~
The full, absolute, path of self in the file system.

``.remove()`` -> None
~~~~~~~~~~~~~~~~~~~~~
Tries to remove self from the file system. On failure it raises a ``FileSystemOperationError``.

``.uri``: str
~~~~~~~~~~~~~
The URI that points to self in the file system.

Directory
---------

``Directory`` extends BaseFileSystemObject_ and specializes to represent directories in the filesystem.

A ``Directory`` extends the BaseFileSystemObject_ interface with:

``.file(`` path: str ``)`` -> File_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns a File_ with its absolute path being the given path relative to self.

``.list()`` -> List[BaseFileSystemObject_]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns the contents of the Directory_ in the file system as a list of BaseFileSystemObject_.

If the Directory_ does not exist the list will be empty.

``.subdir(`` path: str ``)`` -> Directory_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns a Directory_ with its absolute path being the given path relative to self.

File
----

``File`` extends BaseFileSystemObject_ and specializes to represent files in the filesystem.

A ``File`` extends the BaseFileSystemObject_ interface with:

``.read()`` -> bytes
~~~~~~~~~~~~~~~~~~~~
Returns the contents of the File_.

If it fails to read the file a ``FileSystemOperationError`` will be raised.

``.write(`` content: bytes ``)`` -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sets the contents of the File_. If the parent Directory_ does not exist it is created.

If it fails to read the file a ``FileSystemOperationError`` will be raised.


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
