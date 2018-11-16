Examples
========

Public API
----------

.. code:: ipython3

    import norfs.helpers


Filesystem Clients
~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    local_fs_client = norfs.helpers.local()
    memory_fs_client = norfs.helpers.memory()

    import boto3
    s3_fs_client = norfs.helpers.s3(s3_client=boto3.client('s3'))

Files and Directories
~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    cwd = local_fs_client.dir('.')

.. code:: ipython3

    cwd.list()




.. parsed-literal::

    [Directory(fs=LocalFileSystem(), path=/home/jovyan/work/.ipynb_checkpoints),
     File(fs=LocalFileSystem(), path=/home/jovyan/work/Dockerfile),
     File(fs=LocalFileSystem(), path=/home/jovyan/work/Public API.ipynb),
     File(fs=LocalFileSystem(), path=/home/jovyan/work/Untitled.ipynb)]



.. code:: ipython3

    local_file = cwd.file('demo.txt')
    local_file.write(b'Hello norfs!')
    local_file.read()




.. parsed-literal::

    b'Hello norfs!'



.. code:: ipython3

    s3_fs_client.file('myBucket/hello-world.txt').read()




.. parsed-literal::

    b'Hello World!'



.. code:: ipython3

    s3_dir = s3_fs_client.dir('myBucket/norfs-demo/')
    s3_dir.list()




.. parsed-literal::

    []



.. code:: ipython3

    type(local_file)




.. parsed-literal::

    norfs.filesystem.File



.. code:: ipython3

    type(s3_dir.file('a_file.txt'))




.. parsed-literal::

    norfs.filesystem.File



.. code:: ipython3

    type(cwd)




.. parsed-literal::

    norfs.filesystem.Directory



.. code:: ipython3

    type(s3_dir)




.. parsed-literal::

    norfs.filesystem.Directory



Copying
~~~~~~~

.. code:: ipython3

    copy_client = norfs.helpers.get_copy_client(local_fs_client, s3_fs_client, memory_fs_client)

.. code:: ipython3

    copy_client.copy(local_file, s3_dir)

.. code:: ipython3

    s3_dir.list()




.. parsed-literal::

    [File(fs=S3FileSystem(s3_client=<botocore.client.S3 object at 0x7f5b32227e48>, uri_protocol=s3, separator=/), path=myBucket/norfs-demo/demo.txt)]



.. code:: ipython3

    s3_dir.file(local_file.name).read()




.. parsed-literal::

    b'Hello norfs!'


Key Store
---------

.. code:: ipython3

    import norfs.helpers

    local_fs_client = norfs.helpers.local()

    import boto3
    s3_fs_client = norfs.helpers.s3(s3_client=boto3.client('s3'))

.. code:: ipython3

    class Store:

        def __init__(self, store_file):
            self._file = store_file
            self._store = set()

        def __enter__(self):
            if self._file.exists():
                self._store = set(x.decode('utf-8') for x in self._file.read().split(b'\n') if x)

            return self._store

        def __exit__(self, *args):
            self._file.write(b'\n'.join(x.encode('utf-8') for x in self._store if x))

.. code:: ipython3

    store_file = local_fs_client.file('store')

    with Store(store_file) as store:
        for i in range(10):
            store.add(str(i))

    store_file.read()




.. parsed-literal::

    b'0\n7\n8\n6\n3\n2\n1\n9\n5\n4'



.. code:: ipython3

    s3_store_file = s3_fs_client.file('myBucket/norfs-demo/store')

    with Store(s3_store_file) as store:
        for i in range(10):
            store.add(str(i))

    s3_store_file.read()




.. parsed-literal::

    b'0\n7\n8\n6\n3\n2\n1\n9\n5\n4'



From config using URI
~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    class FileFactory:

        def __init__(self, mapping):
            self._mapping = mapping

        def file_from_uri(self, file_uri):
            protocol, path = file_uri.split('://')
            return self._mapping[protocol.lower()].file(path)

.. code:: ipython3

    file_factory = FileFactory({'file': local_fs_client, 's3': s3_fs_client})

.. code:: ipython3

    def main(store_uri):
        store_file = file_factory.file_from_uri(store_uri)

        with Store(store_file) as store:
            for i in range(5, 20):
                store.add(str(i))

        print(store_file.read())

.. code:: ipython3

    main('file://./store')


.. parsed-literal::

    b'15\n0\n8\n7\n17\n13\n10\n6\n16\n19\n11\n3\n2\n12\n14\n18\n1\n9\n5\n4'


.. code:: ipython3

    main('s3://myBucket/norfs-demo/store')


.. parsed-literal::

    b'15\n0\n8\n7\n17\n13\n10\n6\n16\n19\n11\n3\n2\n12\n14\n18\n1\n9\n5\n4'



PySpark
-------

.. code:: ipython3

    import norfs.helpers

    local_fs_client = norfs.helpers.local()

    import boto3
    s3_fs_client = norfs.helpers.s3(s3_client=boto3.client('s3'))

.. code:: ipython3

    from pyspark import SparkContext

    sc = SparkContext.getOrCreate()

.. code:: ipython3

    def spark_count_lines(input_file):
        rdd = sc.textFile(input_file.uri)
        return rdd.count()

.. code:: ipython3

    def init_input_file(input_file):
        input_file.write(b'\n'.join(str(x).encode('utf-8') for x in range(123)))

.. code:: ipython3

    local_file = local_fs_client.file('input_file')
    s3_file = s3_fs_client.file('myBucket/norfs-demo/input_file')

.. code:: ipython3

    init_input_file(local_file)
    spark_count_lines(local_file)




.. parsed-literal::

    123



.. code:: ipython3

    init_input_file(s3_file)
    spark_count_lines(s3_file)




.. parsed-literal::

    123
