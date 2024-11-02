=====================
**aws_administrator**
=====================

Overview
--------

Run AWS administrative scripts.

Usage Example
--------------

Installation:

.. code-block:: BASH

    pip3 install aws_administrator
    # or
    python3 -m pip install aws_administrator

Python:

.. code-block:: PYTHON

    # Prerequisite steps:
    # 1. Copy the parameters/parameters.ini file to your current working directory.
    # 2. Update the file with the necessary values.

    # Get AWS SSO Permission Set details from all accounts.
    from aws_administrator.scripts import aws_sso_get
