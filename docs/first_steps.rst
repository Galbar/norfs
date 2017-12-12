.. _first-steps:

First steps
===========
`norfs` knows of two types of file system objects: `File` and `Directory`.

File
----
`norfs` offers some handy shortcuts to create a File instance of the supported filesystems::

    In[1]: norfs.localfile("path/to/file")
    Out[1]:File(fs=LocalFileSystem(), path=/home/user/path/to/file, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)

    In[2]: norfs.s3file("my_bucket/path/to/file")
    Out[2]:File(fs=S3FileSystem(s3_client=<botocore.client.S3 object at 0x108d8d5f8>, uri_protocol=s3, separator=/), path=my_bucket/path/to/file, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)

    In[3]: norfs.memoryfile("path/to/file")
    Out[3]:File(fs=MemoryFileSystem(root=<norfs.fs.memory.MemoryDirectory object at 0x107dc42b0>), path=path/to/file, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)

Read and write
~~~~~~~~~~~~~~
Files can be read from and written into::

    In[5]: file.read()
    Out[5]:b"contents inside file"

    In[6]: file.write(b"new contents")

    In[7]: file.read()
    Out[7]:b"new contents"

For more documentation see :py:class:`norfs.filesystem.File`.

Directory
---------
`norfs` also offers handy shortcuts to create a Directory instance::

    In[8]: norfs.localdir("some/dir")
    Out[8]:Directory(fs=LocalFileSystem(), path=/Users/alessiolinares/Programs/norfs/some/dir, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)

    In[9]: norfs.s3dir("some/dir")
    Out[9]:Directory(fs=S3FileSystem(s3_client=<botocore.client.S3 object at 0x108d8d5f8>, uri_protocol=s3, separator=/), path=some/dir, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)

    In[10]: norfs.memorydir("some/dir")
    Out[10]:Directory(fs=MemoryFileSystem(root=<norfs.fs.memory.MemoryDirectory object at 0x107dc42b0>), path=some/dir, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)

List directory
~~~~~~~~~~~~~~
A Directory can be listed to retrieve its contents::

    In[12]: dir.list()
    Out[12]:[File(fs=LocalFileSystem(), path=/home/user/some/dir/file, copy_handler=<norfs.copy.CopyHandler object at 0x107cf1908>)]

For more documentation see :py:class:`norfs.filesystem.Directory`.
