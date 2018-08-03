Examples
========


Copy local file to S3
---------------------
::

    import norfs.helpers
    import boto3

    s3 = norfs.helpers.s3(s3_client=boto3.client("s3"))
    local = norfs.helpers.local()
    cp = norfs.helpers.get_copy_client(s3, local)

    local_file = local.file("some/file.txt")
    local_file.write(b'local_file contents')

    s3_dir = s3.dir("myBucket/myDir")

    cp.copy(local_file, s3_dir)

    assert local_file.read() == s3_dir.file("file.txt").read()
