Examples
========


Copy local file to S3
---------------------
::

    import norfs
    import boto3

    norfs.configure(s3_client=boto3.client("s3"))

    local_file = norfs.localfile("some/file.txt")
    local_file.write(b'local_file contents')

    s3_dir = norfs.s3dir("myBucket/myDir")

    local_file.copy(s3_dir)

    assert local_file.read() == s3_dir.file("file.txt").read()
