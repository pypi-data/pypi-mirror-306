=======
PyEALib
=======

Copyright (c) 2014-2024 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)

* Web site: http://www.jdhp.org/software_en.html#ealib
* Online documentation: https://jdhp-dev.gitlab.io/ealib
* Source code: https://gitlab.com/ealib
* Issue tracker: https://gitlab.com/jdhp-dev/ealib/issues
* Pytest code coverage: https://jdhp-dev.gitlab.io/ealib/htmlcov/index.html
* PyEALib on PyPI: https://pypi.org/project/ealib


Description
===========

An open source Python library for mathematical optimization

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

PyEALib requires Python 3.11 (or newer) and Python packages listed in the `requirements.txt` file.


.. _install:

Installation (development environment)
======================================

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the PyEALib source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Windows
-------

From the PyEALib source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Installation (production environment)
=====================================

::

    pip install ealib


Documentation
=============

* Online documentation: https://jdhp-dev.gitlab.io/ealib
* API documentation: https://jdhp-dev.gitlab.io/ealib/api.html


Build and run the Python Docker image
=====================================

Build the docker image
----------------------

From the PyEALib source code::

    docker build -t ealib:latest .

Run unit tests from the docker container
----------------------------------------

From the PyEALib source code::

    docker run ealib pytest

Run an example from the docker container
----------------------------------------

From the PyEALib source code::

    docker run ealib python3 /app/examples/hello.py


Bug reports
===========

To search for bugs or report them, please use the PyEALib Bug Tracker at:

    https://gitlab.com/jdhp-dev/ealib/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe