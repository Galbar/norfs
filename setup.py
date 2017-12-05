from setuptools import setup, find_packages

VERSION = "1.0.0"

setup(name="norfs",
      version=VERSION,
      author="Alessio Linares",
      author_email="alessio@alessio.cc",
      description=("Normalized filesystem. "
                   "This library offers a common interface to interact with multiple filesystems, local or remote."),
      keywords=["filesystem", "boto", "s3", "file", "directory", "norfs"],
      url="https://github.com/Galbar/norfs",
      download_url="https://github.com/Galbar/norfs/archive/{}.tar.gz".format(VERSION),
      license='MIT',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 5 - Production/Stable',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      python_requires='>=3.6',
      packages=find_packages(exclude=["tests"]))
