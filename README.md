norfs
=============

**Nor**malized **f**ile**s**ystem. This library offers a common interface to interact with multiple filesystems,
local or remote.

Features
========
Supported filesystems:
 * Local filesystem
 * S3
 * In-memory

Supported operations:
 * File and Directory
   * Check if it exists
   * Copy
   * Name
   * Parent directory
   * Path
   * Remove
   * URI
 * File
   * Read binary
   * Write binary
 * Directory
   * List

Example
=======

```python
In [1]: import norfs

In [2]: local_file = norfs.localfile("some/file.txt")

In [3]: local_dir = norfs.localdir("some")

In [4]: local_dir.exists()
Out[4]: False

In [5]: local_file.write(b"contents")

In [6]: local_dir.exists()
Out[6]: True

In [7]: local_file.read()
Out[7]: b'contents'

In [8]: import boto3

In [9]: norfs.configure(s3_client=boto3.client("s3"))

In [10]: s3_dir = norfs.s3dir("myBucket", "some")

In [11]: s3_dir.exists()
Out[11]: False

In [12]: local_dir.copy(s3_dir)

In [13]: s3_dir.exists()
Out[13]: True

In [14]: s3_dir.file("file.txt").read()
Out[14]: b'contents'

In [15]: mem_file = norfs.memoryfile("file/in/memory.txt")

In [16]: mem_file.exists()
Out[16]: False

In [17]: mem_file.parent().path
Out[17]: 'file/in'

In [18]: mem_file.parent().exists()
Out[18]: False

In [19]: mem_file.write(s3_dir.file("file.txt").read())

In [20]: mem_file.parent().list()
Out[20]: [File(fs=MemoryFileSystem(root=<norfs.fs.memory.MemoryDirectory object at 0x10f62e8d0>), path=file/in/memory.txt, copy_handler=<norfs.copy.CopyHandler object at 0x10eba79e8>)]

In [21]: mem_file.read()
Out[21]: b'contents'
```
