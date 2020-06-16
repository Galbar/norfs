norfs
=====

|Build Status| |Coverage Status| |PyPI Status| |PyPI Version| |PyPI Python| 
|PyPI License| |PyPI Format|

**Nor**\ malized **f**\ ile\ **s**\ ystem. This library offers a common
interface to interact with multiple filesystems, local or remote::

    import norfs.helpers

    local = norfs.helpers.local()
    demo_file = local.file('demo.txt')
    demo_file.write(b'Hello World')
    print(demo_file.read())


Install with ``pip``: ``pip install norfs``.

Find more information in the `documentation`_

.. _documentation: https://galbar.github.io/norfs

.. |Build Status| image:: https://travis-ci.org/Galbar/norfs.svg?branch=master
   :target: https://travis-ci.org/Galbar/norfs
.. |Coverage Status| image:: https://coveralls.io/repos/github/Galbar/norfs/badge.svg?branch=master
   :target: https://coveralls.io/github/Galbar/norfs?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/norfs/badge/?version=latest
   :target: http://norfs.readthedocs.io/en/latest/?badge=latest
.. |PyPI Status| image:: https://img.shields.io/pypi/status/norfs.svg
   :target: https://pypi.python.org/pypi/norfs/
.. |PyPI Version| image:: https://img.shields.io/pypi/v/norfs.svg
   :target: https://pypi.python.org/pypi/norfs/
.. |PyPI Python| image:: https://img.shields.io/pypi/pyversions/norfs.svg
   :target: https://pypi.python.org/pypi/norfs/
.. |PyPI License| image:: https://img.shields.io/pypi/l/norfs.svg
   :target: https://pypi.python.org/pypi/norfs/
.. |PyPI Format| image:: https://img.shields.io/pypi/format/norfs.svg
   :target: https://pypi.python.org/pypi/norfs/
