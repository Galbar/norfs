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

The most public interface norfs exposes is composed of the FileSystemClient_, the CopyClient_ and the BaseFileSystemObject_ with its subclasses Directory_ an File_.

FileSystemClient
----------------

``FileSystemClient`` provides a way to access the file system objects of a given file system. It is a handy class that 
provides easy access to File_ and Directory_ instances. It is usually obtained using the ``norfs.helpers``::

    import norfs.helpers

    local_fs_client = norfs.helpers.local()

    memory_fs_client = norfs.helpers.memory()

    import boto3
    s3_fs_client = norfs.helpers.s3(s3_client=boto3.client('s3'))

A ``FileSystemClient`` exposes the following interface:

``.dir(`` path: str ``)`` -> Directory_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns a Directory_ instance for the given path.

``.file(`` path: str ``)`` -> File_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns a File_ instance for the given path.

``.fs`` -> norfs.fs.base.BaseFileSystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns a the BaseFileSystemObject_ the client is managing.


CopyClient
----------

``CopyClient`` provides a unified simple copy API for any File_ or Directory_ from any file system. It is usually 
accessed by using ``norfs.helpers.get_copy_client()``::

    import norfs.helpers

    local = norfs.helpers.local()
    cp_local_only = norfs.helpers.get_copy_client(local)

    cp_local_only.copy(local.file('source_file.txt'), local.file('target_file.txt'))


    memory = norfs.helpers.memory()

    import boto3
    s3 = norfs.helpers.s3(s3_client=boto3.client('s3'))

    cp_for_all = norfs.helpers.get_copy_client(local, s3, memory)

    cp_for_all.copy(s3.file('myBucket/source_file.txt'), local.file('target_file.txt'))

``norfs.helpers.get_copy_client()`` returns a CopyClient_ instance configured with copy strategies for each of the 
file system clients passed. A ``norfs.copy.base.Copier`` can have copy policies set for a pair of source and 
destination file systems to implement a better strategy of copying between them than read source and write 
destination. ``norfs.helpers.get_copy_client()`` helps you by setting these for you.

A ``CopyClient`` exposes the following interface:

``.copy(`` src: BaseFileSystemObject_, dst: BaseFileSystemObject_ ``)`` -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Copies ``src`` to ``dst``, no mater the file systems they are on. ``src`` and ``dst`` can by both File_ or Directory_. 
The only operation not supported is copying from a Directory_ into a File_ as it does not make sense.

If source is a Directory_ and destination is a File_ it raises a ``TypeError``.

On copy failure it raises a ``FileSystemOperationError``.

``.copier`` -> norfs.copy.base.Copier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns the ``Copier`` instance that the client manages.


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
